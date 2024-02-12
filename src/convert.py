import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
import yaml
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name, get_file_name_with_ext
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    train_images_path = "/home/alex/DATASETS/TODO/BSTLD/train/rgb/train"
    train_ann_yaml = "/home/alex/DATASETS/TODO/BSTLD/train/train.yaml"

    test_images_path = "/home/alex/DATASETS/TODO/BSTLD/test/rgb/test"
    test_ann_yaml = "/home/alex/DATASETS/TODO/BSTLD/test/test.yaml"
    batch_size = 30

    def create_ann(image_path):
        labels = []
        tags = []

        img_wight = 1280
        img_height = 720

        if ds_name == "train":
            seq_value = image_path.split("/")[-2]
            seq_meta = meta.get_tag_meta(seq_value)
            seq = sly.Tag(seq_meta)
            tags.append(seq)

        bbox_data = im_name_to_bboxes[get_file_name(image_path)]
        for curr_bbox_data in bbox_data:
            label_tags = []

            name = curr_bbox_data["label"]
            obj_class = color_to_class[name]
            direction_meta = direction_to_meta.get(name)
            if direction_meta is not None:
                direction = sly.Tag(direction_meta)
                label_tags.append(direction)
            occluded_value = curr_bbox_data["occluded"]
            if occluded_value:
                occluded = sly.Tag(occluded_meta)
                label_tags.append(occluded)

            top = int(curr_bbox_data["y_min"])
            left = int(curr_bbox_data["x_min"])
            bottom = int(curr_bbox_data["y_max"])
            right = int(curr_bbox_data["x_max"])

            if top > bottom or left > right:
                continue

            rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
            label = sly.Label(rect, obj_class, tags=label_tags)
            labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    red = sly.ObjClass("red", sly.Rectangle)
    yellow = sly.ObjClass("yellow", sly.Rectangle)
    green = sly.ObjClass("green", sly.Rectangle)
    off = sly.ObjClass("off", sly.Rectangle)

    color_to_class = {
        "Green": green,
        "RedLeft": red,
        "Yellow": yellow,
        "GreenLeft": green,
        "Red": red,
        "off": off,
        "GreenRight": green,
        "GreenStraight": green,
        "RedRight": red,
        "RedStraight": red,
        "GreenStraightLeft": green,
        "GreenStraightRight": green,
        "RedStraightLeft": red,
    }

    occluded_meta = sly.TagMeta("occluded", sly.TagValueType.NONE)
    seq1_meta = sly.TagMeta(
        "2015-05-29-15-29-39_arastradero_traffic_light_loop_bag", sly.TagValueType.NONE
    )
    seq2_meta = sly.TagMeta("2015-10-05-10-52-01_bag", sly.TagValueType.NONE)
    seq3_meta = sly.TagMeta("2015-10-05-10-55-33_bag", sly.TagValueType.NONE)
    seq4_meta = sly.TagMeta("2015-10-05-11-26-32_bag", sly.TagValueType.NONE)
    seq5_meta = sly.TagMeta("2015-10-05-14-40-46_bag", sly.TagValueType.NONE)
    seq6_meta = sly.TagMeta("2015-10-05-16-02-30_bag", sly.TagValueType.NONE)
    seq7_meta = sly.TagMeta(
        "2017-02-03-11-44-56_los_altos_mountain_view_traffic_lights_bag", sly.TagValueType.NONE
    )

    left_meta = sly.TagMeta("left", sly.TagValueType.NONE)
    straight_meta = sly.TagMeta("straight", sly.TagValueType.NONE)
    right_meta = sly.TagMeta("right", sly.TagValueType.NONE)
    straight_l_meta = sly.TagMeta("straight left", sly.TagValueType.NONE)
    straight_r_meta = sly.TagMeta("straight right", sly.TagValueType.NONE)

    direction_to_meta = {
        "RedLeft": left_meta,
        "GreenLeft": left_meta,
        "GreenRight": right_meta,
        "GreenStraight": straight_meta,
        "RedRight": right_meta,
        "RedStraight": straight_meta,
        "GreenStraightLeft": straight_l_meta,
        "GreenStraightRight": straight_r_meta,
        "RedStraightLeft": straight_l_meta,
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    meta = sly.ProjectMeta(
        obj_classes=[red, yellow, green, off],
        tag_metas=[
            seq1_meta,
            seq2_meta,
            seq3_meta,
            seq4_meta,
            seq5_meta,
            seq6_meta,
            seq7_meta,
            occluded_meta,
            left_meta,
            straight_meta,
            right_meta,
            straight_l_meta,
            straight_r_meta,
        ],
    )

    api.project.update_meta(project.id, meta.to_json())

    train_images_pathes = glob.glob(train_images_path + "/*/*.png")
    test_images_pathes = glob.glob(test_images_path + "/*.png")

    ds_name_to_data = {
        "train": (train_images_pathes, train_ann_yaml),
        "test": (test_images_pathes, test_ann_yaml),
    }

    for ds_name, ds_data in ds_name_to_data.items():

        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        all_images, ann_path = ds_data

        im_name_to_bboxes = {}

        with open(ann_path, "r") as stream:
            ann_data = yaml.safe_load(stream)
            for curr_ann_data in ann_data:
                im_name_to_bboxes[get_file_name(curr_ann_data["path"])] = curr_ann_data["boxes"]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(all_images))

        for img_pathes_batch in sly.batched(all_images, batch_size=batch_size):
            img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_names_batch))

    return project
