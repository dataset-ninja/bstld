Dataset **BSTLD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/J/c/A8/iTfWA1QUPXUYQRXBZcO4b1wGLrsv45yh6QQRnbm0nLrMPVZ42GlW1LYqueZNnQ5WPW4dFjRRn0HdhrqW3SbaiXgLv0MKgsKBLdj14M4G76l4BQiUAiBfNqJ4HXsW.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='BSTLD', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://github.com/bosch-ros-pkg/bstld/tree/master/label_files).