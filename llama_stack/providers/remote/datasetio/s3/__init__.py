# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from .config import S3DatasetIOConfig


async def get_adapter_impl(config: S3DatasetIOConfig):
    from .s3 import S3DatasetIOImpl

    return S3DatasetIOImpl(config)
