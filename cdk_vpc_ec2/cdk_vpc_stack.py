from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class CdkVpcStack(Stack):
    
    @property
    def availability_zones(self):
        return ['ap-northeast-2a', 'ap-northeast-2c']

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=2,
                           cidr="10.10.0.0/16",
                           # configuration will create 3 groups in 2 AZs = 6 subnets.
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="Public",
                               cidr_mask=25
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                               name="Private",
                               cidr_mask=25
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                               name="DB",
                               cidr_mask=25
                           )
                           ],
                           # nat_gateway_provider=ec2.NatProvider.gateway(),
                           nat_gateways=1,
                           )
        CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)
                       
        for i, subnet in enumerate(self.vpc.public_subnets):
            subnet.node.default_child.add_property_override('CidrBlock', f'10.10.1.{128 * i}/25')
            
        for i, subnet in enumerate(self.vpc.private_subnets):
            subnet.node.default_child.add_property_override('CidrBlock', f'10.10.10.{128 * i}/25')
            
        for i, subnet in enumerate(self.vpc.isolated_subnets):
            subnet.node.default_child.add_property_override('CidrBlock', f'10.10.100.{128 * i}/25')
