# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.
from typing import Optional

import boto3

from llama_stack.apis.datasets import Dataset, Datasets

from .config import S3DatasetIOConfig


class S3DatasetIOImpl(Datasets):
    def __init__(self, config: S3DatasetIOConfig) -> None:
        self.config = config
        self.client = boto3.client("s3")

    async def get_dataset(
        self,
        dataset_id: str,
    ) -> Optional[Dataset]: ...

    async def list_datasets(self):
        return []

    async def register_dataset(
        self,
        dataset: Dataset,
    ) -> None:
        try:
            self.client.head_object(Bucket=self.config.bucketName, Key=self.s3_key(dataset.dataset_id))
            raise ValueError(f"Dataset with id {dataset.dataset_id} already exists")
        except self.client.exceptions.ClientError as e:
            if e.response["Error"]["Code"] != "404":
                raise
        self.client.put_object(
            Bucket=self.config.bucketName,
            Key=self.s3_key(dataset.dataset_id),
            Body=dataset.model_dump_json(),
        )

    async def unregister_dataset(self, dataset_id: str) -> None:
        try:
            self.client.delete_object(Bucket=self.config.bucketName, Key=self.s3_key(dataset_id))
        except self.client.exceptions.ClientError as e:
            if e.response["Error"]["Code"] != "404":
                raise

    def s3_key(self, dataset_id: str) -> str:
        return f"datasets/{dataset_id}.json"
