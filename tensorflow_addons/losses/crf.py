# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Implementing Conditional Random Field loss."""

from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow_addons.layers.crf import CRF


@tf.keras.utils.register_keras_serializable(package="Addons")
class ConditionalRandomFieldLoss(object):
    def __init__(self, name="crf_loss"):
        self.name = name

    def get_config(self):
        return {"name": self.name}

    def __call__(self, y_true, y_pred, sample_weight=None):
        crf_layer = y_pred._keras_history[0]

        # check if last layer is CRF
        if not isinstance(crf_layer, CRF):
            raise ValueError(
                "Last layer must be CRF for use {}.".format(self.__class__.__name__)
            )

        loss_vector = crf_layer.get_loss(y_true, y_pred)

        return tf.keras.backend.mean(loss_vector)


@tf.keras.utils.register_keras_serializable(package="Addons")
def crf_loss(y_true, y_pred):
    """
    Args
        y_true: true targets tensor.
        y_pred: predictions tensor.

    Returns:
        scalar.
    """
    crf_layer = y_pred._keras_history[0]

    # check if last layer is CRF
    if not isinstance(crf_layer, CRF):
        raise ValueError("Last layer must be CRF for use {}.".format("crf_loss"))

    loss_vector = crf_layer.get_loss(y_true, y_pred)

    return tf.keras.backend.mean(loss_vector)