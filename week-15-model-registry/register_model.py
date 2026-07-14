"""
register_model.py — real Model Registry registration via boto3

WHY THIS EXISTS: SageMaker's ModelStep/RegisterModel step type is NOT
supported in local mode (confirmed error: "Step type RegisterModel is not
supported in local mode"). Registration itself is just a lightweight
metadata API call (CreateModelPackage) -- it needs no compute instance and
no quota. So instead of the SDK's ModelStep abstraction, this script calls
the same underlying AWS API directly via boto3, running inside a plain
ProcessingStep (which local mode DOES support).
"""
import argparse
import boto3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-s3-uri", type=str, required=True)
    parser.add_argument("--image-uri", type=str, required=True)
    parser.add_argument("--model-package-group-name", type=str, default="aria-classifier-models")
    args = parser.parse_args()

    sm = boto3.client("sagemaker", region_name="us-east-1")

    print(f"Registering model package into group: {args.model_package_group_name}")
    print(f"Model artifact: {args.model_s3_uri}")

    response = sm.create_model_package(
        ModelPackageGroupName=args.model_package_group_name,
        # A human (or a future automated approval step) decides deployability
        # -- the pipeline never auto-approves. This is the real governance
        # gate before anything reaches production.
        ModelApprovalStatus="PendingManualApproval",
        InferenceSpecification={
            "Containers": [
                {"Image": args.image_uri, "ModelDataUrl": args.model_s3_uri}
            ],
            "SupportedContentTypes": ["application/json"],
            "SupportedResponseMIMETypes": ["application/json"],
            "SupportedRealtimeInferenceInstanceTypes": ["ml.m5.large"],
            "SupportedTransformInstanceTypes": ["ml.m5.large"],
        },
    )

    print(f"Registered model package: {response['ModelPackageArn']}")


if __name__ == "__main__":
    main()