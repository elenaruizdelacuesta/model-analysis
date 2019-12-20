# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Defines Fairness Indicator's Jupyter notebook widgets."""
import ipywidgets as widgets
from traitlets import Unicode


@widgets.register
class FairnessIndicatorViewer(widgets.DOMWidget):
  """The fairness indicator visualization widget."""
  _view_name = Unicode('FairnessIndicatorView').tag(sync=True)
  _view_module = Unicode('tfma_widget_js').tag(sync=True)
  _view_module_version = Unicode('0.1.0').tag(sync=True)
  _model_name = Unicode('FairnessIndicatorModel').tag(sync=True)
  _model_module = Unicode('tfma_widget_js').tag(sync=True)
  _model_module_version = Unicode('0.1.0').tag(sync=True)
  value = Unicode('Hello World!').tag(sync=True)
