# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.
import os

from pydantic import BaseModel


class S3DatasetIOConfig(BaseModel):
    bucket_name = os.getenv("S3_BUCKET_NAME")
    if bucket_name is None:
        raise ValueError("S3_BUCKET_NAME environment variable must be set")
