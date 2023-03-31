import unittest

from glitch.analysis.security import SecurityVisitor
from glitch.parsers.cmof import TerraformParser
from glitch.tech import Tech

class TestSecurity(unittest.TestCase):
    def __help_test(self, path, n_errors, codes, lines):
        parser = TerraformParser()
        inter = parser.parse(path, "script", False)
        analysis = SecurityVisitor(Tech.terraform)
        analysis.config("configs/default.ini")
        errors = list(filter(lambda e: e.code.startswith('sec_'), set(analysis.check(inter))))
        errors = sorted(errors, key=lambda e: (e.path, e.line, e.code))
        self.assertEqual(len(errors), n_errors)
        for i in range(n_errors):
            self.assertEqual(errors[i].code, codes[i])
            self.assertEqual(errors[i].line, lines[i])  

    # testing previous implemented code smells
    def test_terraform_http(self):
        self.__help_test(
            "tests/security/terraform/files/http.tf",
            1, ["sec_https"], [2]
        )

    def test_terraform_susp_comment(self):
        self.__help_test(
            "tests/security/terraform/files/susp.tf",
            1, ["sec_susp_comm"], [8]
        )

    def test_terraform_def_admin(self):
        self.__help_test(
            "tests/security/terraform/files/admin.tf",
            3, ["sec_def_admin", "sec_hard_secr", "sec_hard_user"], [2, 2, 2]
        )

    def test_terraform_empt_pass(self):
        self.__help_test(
            "tests/security/terraform/files/empty.tf",
            3, ["sec_empty_pass", "sec_hard_pass", "sec_hard_secr"], [5, 5, 5]
        )

    def test_terraform_weak_crypt(self):
        self.__help_test(
            "tests/security/terraform/files/weak_crypt.tf",
            1, ["sec_weak_crypt"], [4]
        )

    def test_terraform_hard_secr(self):
        self.__help_test(
            "tests/security/terraform/files/hard_secr.tf",
            2, 
            ["sec_hard_pass", "sec_hard_secr"]
            , [5, 5]
        )

    def test_terraform_invalid_bind(self):
        self.__help_test(
            "tests/security/terraform/files/inv_bind.tf",
            1, ["sec_invalid_bind"], [19]
        )

    # testing new implemented code smells, or previous ones with new rules for Terraform

    def test_terraform_insecure_access_control(self):
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/access-to-bigquery-dataset.tf",
            1, ["sec_access_control"], [3]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/aks-ip-ranges-enabled.tf",
            1, ["sec_access_control"], [1]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/associated-access-block-to-s3-bucket.tf",
            1, ["sec_access_control"], [1]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/aws-database-instance-publicly-accessible.tf",
            2, ["sec_access_control", "sec_access_control"], [2, 16]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/aws-sqs-no-wildcards-in-policy.tf",
            1, ["sec_access_control"], [4]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/azure-authorization-wildcard-action.tf",
            1, ["sec_access_control"], [7]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/azure-container-use-rbac-permissions.tf",
            1, ["sec_access_control"], [2]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/azure-database-not-publicly-accessible.tf",
            2, ["sec_access_control", "sec_access_control"], [1, 6]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/bucket-public-read-acl.tf",
            3, ["sec_access_control", "sec_access_control", "sec_access_control"], [1, 8, 25]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/cidr-range-public-access-eks-cluster.tf",
            1, ["sec_access_control"], [1]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/cross-db-ownership-chaining.tf",
            3, ["sec_access_control", "sec_access_control", "sec_access_control"], [1, 50, 97]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/data-factory-public-access.tf",
            2, ["sec_access_control", "sec_access_control"], [1, 5]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/google-compute-no-default-service-account.tf",
            2, ["sec_access_control", "sec_access_control"], [1, 19]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/google-gke-use-rbac-permissions.tf",
            1, ["sec_access_control"], [14]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/google-storage-enable-ubla.tf",
            2, ["sec_access_control", "sec_access_control"], [1, 5]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/google-storage-no-public-access.tf",
            3, ["sec_access_control", "sec_access_control", "sec_access_control"], [4, 10, 22]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/mq-broker-publicly-exposed.tf",
            1, ["sec_access_control"], [2]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/prevent-client-disable-encryption.tf",
            1, ["sec_access_control"], [13]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/private-cluster-nodes.tf",
            2, ["sec_access_control", "sec_access_control"], [1, 16]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/public-access-eks-cluster.tf",
            1, ["sec_access_control"], [10]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/public-access-policy.tf",
            1, ["sec_access_control"], [4]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/public-github-repo.tf",
            3, ["sec_access_control", "sec_access_control", "sec_access_control"], [1, 6, 18]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/s3-access-through-acl.tf",
            1, ["sec_access_control"], [7]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/s3-block-public-acl.tf",
            2, ["sec_access_control", "sec_access_control"], [1, 10]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/s3-block-public-policy.tf",
            2, ["sec_access_control", "sec_access_control"], [1, 11]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/s3-ignore-public-acl.tf",
            2, ["sec_access_control", "sec_access_control"], [1, 13]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/s3-restrict-public-bucket.tf",
            2, ["sec_access_control", "sec_access_control"], [1, 12]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/specify-source-lambda-permission.tf",
            1, ["sec_access_control"], [1]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/storage-containers-public-access.tf",
            1, ["sec_access_control"], [26]
        )
        self.__help_test(
            "tests/security/terraform/files/insecure-access-control/unauthorized-access-api-gateway-methods.tf",
            2, ["sec_access_control", "sec_access_control"], [37, 44]
        )

    def test_terraform_invalid_ip_binding(self):
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/aws-ec2-vpc-no-public-egress-sgr.tf",
            2, ["sec_invalid_bind", "sec_invalid_bind"], [5, 20]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/aws-ec2-vpc-no-public-ingress-acl.tf",
            1, ["sec_invalid_bind"], [7]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/aws-ec2-vpc-no-public-ingress-sgr.tf",
            2, ["sec_invalid_bind", "sec_invalid_bind"], [4, 17]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/azure-network-no-public-egress.tf",
            1, ["sec_invalid_bind"], [3]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/azure-network-no-public-ingress.tf",
            1, ["sec_invalid_bind"], [3]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/cloud-sql-database-publicly-exposed.tf",
            1, ["sec_invalid_bind"], [14]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/compute-firewall-inbound-rule-public-ip.tf",
            1, ["sec_invalid_bind"], [9]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/compute-firewall-outbound-rule-public-ip.tf",
            1, ["sec_invalid_bind"], [9]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/eks-cluster-open-cidr-range.tf",
            1, ["sec_invalid_bind"], [11]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/gke-control-plane-publicly-accessible.tf",
            1, ["sec_invalid_bind"], [8]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/openstack-networking-no-public-egress.tf",
            1, ["sec_invalid_bind"], [8]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/openstack-networking-no-public-ingress.tf",
            1, ["sec_invalid_bind"], [8]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/public-egress-network-policy.tf",
            1, ["sec_invalid_bind"], [27]
        )
        self.__help_test(
            "tests/security/terraform/files/invalid-ip-binding/public-ingress-network-policy.tf",
            1, ["sec_invalid_bind"], [27]
        )

    def test_terraform_disabled_authentication(self):
        self.__help_test(
            "tests/security/terraform/files/disabled-authentication/azure-app-service-authentication-activated.tf",
            2, ["sec_authentication", "sec_authentication"], [1, 11]
        )
        self.__help_test(
            "tests/security/terraform/files/disabled-authentication/contained-database-disabled.tf",
            1, ["sec_authentication"], [1]
        )
        self.__help_test(
            "tests/security/terraform/files/disabled-authentication/disable-password-authentication.tf",
            3, ["sec_authentication", "sec_authentication", "sec_authentication"], [2, 13, 18]
        )
        self.__help_test(
            "tests/security/terraform/files/disabled-authentication/gke-basic-auth.tf",
            1, ["sec_authentication"], [4]
        )
        self.__help_test(
            "tests/security/terraform/files/disabled-authentication/iam-group-with-mfa.tf",
            2, ["sec_authentication", "sec_authentication"], [7, 53]
        )

    def test_terraform_missing_encryption(self):
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/athena-enable-at-rest-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 10]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/aws-codebuild-enable-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [3, 9]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/aws-ecr-encrypted.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 13]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/aws-neptune-at-rest-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 9]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/documentdb-storage-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 9]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/dynamodb-rest-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 9]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/ecs-task-definitions-in-transit-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 29]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/efs-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 6]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/eks-encryption-secrets-enabled.tf",
            5, ["sec_missing_encryption", "sec_missing_encryption", "sec_missing_encryption", "sec_missing_encryption",
                "sec_missing_encryption"], [1, 1, 9, 23, 34]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/elasticache-enable-at-rest-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 6]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/elasticache-enable-in-transit-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 7]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/elasticsearch-domain-encrypted.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 17]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/elasticsearch-in-transit-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 16]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/emr-enable-at-rest-encryption.tf",
            1, ["sec_missing_encryption"], [4]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/emr-enable-in-transit-encryption.tf",
            1, ["sec_missing_encryption"], [4]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/emr-enable-local-disk-encryption.tf",
            1, ["sec_missing_encryption"], [4]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/emr-s3encryption-mode-sse-kms.tf",
            1, ["sec_missing_encryption"], [4]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/enable-cache-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 6]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/encrypted-ebs-volume.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 7]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/encrypted-root-block-device.tf",
            3, ["sec_missing_encryption", "sec_missing_encryption", "sec_missing_encryption"], [1, 13, 23]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/instance-encrypted-block-device.tf",
            1, ["sec_missing_encryption"], [14]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/kinesis-stream-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 6]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/msk-enable-in-transit-encryption.tf",
            3, ["sec_missing_encryption", "sec_missing_encryption", "sec_missing_encryption"], [1, 14, 15]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/rds-encrypt-cluster-storage-data.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 6]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/rds-encrypt-instance-storage-data.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 7]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/redshift-cluster-rest-encryption.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 6]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/unencrypted-s3-bucket.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [25, 64]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/unencrypted-sns-topic.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 5]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/unencrypted-sqs-queue.tf",
            2, ["sec_missing_encryption", "sec_missing_encryption"], [1, 5]
        )
        self.__help_test(
            "tests/security/terraform/files/missing-encryption/workspaces-disk-encryption.tf",
            6, ["sec_missing_encryption", "sec_missing_encryption", "sec_missing_encryption", "sec_missing_encryption", 
                "sec_missing_encryption", "sec_missing_encryption"], [1, 1, 4, 8, 13, 14]
        )

    def test_terraform_hard_coded_secrets(self):
        self.__help_test(
            "tests/security/terraform/files/hard-coded-secrets/encryption-key-in-plaintext.tf",
            1, ["sec_hard_secr"], [3]
        )
        self.__help_test(
            "tests/security/terraform/files/hard-coded-secrets/plaintext-password.tf",
            2, ["sec_hard_pass", "sec_hard_secr"], [2, 2]
        )
        self.__help_test(
            "tests/security/terraform/files/hard-coded-secrets/plaintext-value-github-actions.tf",
            1, ["sec_hard_secr"], [5]
        )
        self.__help_test(
            "tests/security/terraform/files/hard-coded-secrets/sensitive-credentials-in-vm-custom-data.tf",
            2, ["sec_hard_pass", "sec_hard_secr"], [3, 3]
        )
        self.__help_test(
            "tests/security/terraform/files/hard-coded-secrets/sensitive-data-in-plaintext.tf",
            2, ["sec_hard_pass", "sec_hard_secr"], [8, 8]
        )
        self.__help_test(
            "tests/security/terraform/files/hard-coded-secrets/sensitive-data-stored-in-user-data.tf",
            4, ["sec_hard_pass", "sec_hard_secr", "sec_hard_pass", "sec_hard_secr"], [2, 2, 14, 14]
        )
        self.__help_test(
            "tests/security/terraform/files/hard-coded-secrets/sensitive-environment-variables.tf",
            2, ["sec_hard_pass", "sec_hard_secr"], [2, 2]
        )
        self.__help_test(
            "tests/security/terraform/files/hard-coded-secrets/user-data-contains-sensitive-aws-keys.tf",
            1, ["sec_hard_secr"], [9]
        )

    def test_terraform_public_ip(self):
        self.__help_test(
            "tests/security/terraform/files/public-ip/google-compute-intance-with-public-ip.tf",
            1, ["sec_public_ip"], [4]
        )
        self.__help_test(
            "tests/security/terraform/files/public-ip/lauch-configuration-public-ip-addr.tf",
            1, ["sec_public_ip"], [2]
        )
        self.__help_test(
            "tests/security/terraform/files/public-ip/oracle-compute-no-public-ip.tf",
            1, ["sec_public_ip"], [3]
        )
        self.__help_test(
            "tests/security/terraform/files/public-ip/subnet-public-ip-address.tf",
            1, ["sec_public_ip"], [3]
        )
        
    def test_terraform_use_of_http_without_tls(self):
        self.__help_test(
            "tests/security/terraform/files/use-of-http-without-tls/azure-appservice-enforce-https.tf",
            2, ["sec_https", "sec_https"], [1, 8]
        )
        self.__help_test(
            "tests/security/terraform/files/use-of-http-without-tls/azure-storage-enforce-https.tf",
            1, ["sec_https"], [2]
        )
        self.__help_test(
            "tests/security/terraform/files/use-of-http-without-tls/cloudfront-enforce-https.tf",
            2, ["sec_https", "sec_https"], [1, 13]
        )
        self.__help_test(
            "tests/security/terraform/files/use-of-http-without-tls/digitalocean-compute-enforce-https.tf",
            1, ["sec_https"], [7]
        )
        self.__help_test(
            "tests/security/terraform/files/use-of-http-without-tls/elastic-search-enforce-https.tf",
            2, ["sec_https", "sec_https"], [1, 19]
        )
        self.__help_test(
            "tests/security/terraform/files/use-of-http-without-tls/elb-use-plain-http.tf",
            2, ["sec_https", "sec_https"], [1, 6]
        )


if __name__ == '__main__':
    unittest.main()