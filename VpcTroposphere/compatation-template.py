from troposphere import Template, GetAtt, Join, Ref, Output, Parameter, Tags, Base64, FindInMap
from troposphere.ec2 import VPC, Subnet, RouteTable, NetworkAcl, InternetGateway
from troposphere.ec2 import NatGateway, SubnetNetworkAclAssociation, SubnetRouteTableAssociation
from troposphere.ec2 import VPCGatewayAttachment, Route, EIP, NetworkAclEntry


t = Template()

version = t.add_version("2010-09-09")

Description = t.set_description("""\
        AWS Cloudformation template for competitions project.
        """)

vpcnametag = t.add_parameter(Parameter(
            "VPCName",
            Type="String",
            Description="VPC Name as per project Naming Convension"
            ))

vpccidr = t.add_parameter(Parameter(
            "VPCCIDR",
            Type="String",
            Description="IP Address range for VPC",
            Default="10.0.0.0/16",
            MinLength="9",
            AllowedPattern=r"(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            MaxLength="15"
            ))

subnetpublic1name = t.add_parameter(Parameter(
            "subnetPublic1Name",
            Type="String",
            Description="Subnet Name as per project Naming Convension for Public1"
            ))

subnetcidrpublic1 = t.add_parameter(Parameter(
            "subnetCIRDPublic1",
            Type="String",
            Description="IP Address range for Public1 Subnet",
            Default="10.0.1.0/24"
            ))

subnetpublic2name = t.add_parameter(Parameter(
            "subnetPublic2Name",
            Type="String",
            Description="Subnet Name as per project Naming Convension for Public2"
            ))

subnetcidrpublic2 = t.add_parameter(Parameter(
            "subnetCIRDPublic2",
            Type="String",
            Description="IP Address range for Public2 Subnet",
            Default="10.0.2.0/24"
            ))

subnetprivate1name = t.add_parameter(Parameter(
            "subnetPrivate1Name",
            Type="String",
            Description="Subnet Name as per project Naming Convension for Private1"
            ))

subnetcidrprivate1 = t.add_parameter(Parameter(
            "subnetCIRDPrivate1",
            Type="String",
            Description="IP Address range for Private1 Subnet",
            Default="10.0.3.0/24"
            ))

subnetprivate2name = t.add_parameter(Parameter(
            "subnetPrivate2Name",
            Type="String",
            Description="Subnet Name as per project Naming Convension for Private2"
            ))

subnetcidrprivate2 = t.add_parameter(Parameter(
            "subnetCIRDPrivate2",
            Type="String",
            Description="IP Address range for Private2 Subnet",
            Default="10.0.4.0/24"
            ))

networkaclpublicname = t.add_parameter(Parameter(
            "NetworkAclPublicName",
            Type="String",
            Description="NetworkAcl Name as per project Naming Convension"
            ))

networkaclprivatename = t.add_parameter(Parameter(
            "NetworkAclPrivateName",
            Type="String",
            Description="NetworkAcl Name as per project Naming Convension"
            ))

routetablepublicname = t.add_parameter(Parameter(
            "PublicRouteTableName",
            Type="String",
            Description="RouteTable Name as per project Naming Convension"
            ))

routetableprivatename = t.add_parameter(Parameter(
            "PrivateRouteTableName",
            Type="String",
            Description="RouteTable Name as per project Naming Convension"
            ))

internetgatewayname = t.add_parameter(Parameter(
            "InternetGatewayName",
            Type="String",
            Description="Internet Gateway Name as per project Naming Convension"
            ))

natgatewayname = t.add_parameter(Parameter(
            "NatGatewayName",
            Type="String",
            Description="NatGateway Name as per project Naming Convension"
            ))

vpc = t.add_resource(VPC(
            "VPC",
            CidrBlock=Ref(vpccidr),
            EnableDnsSupport="true",
            EnableDnsHostnames="true",
            Tags=Tags(
                Name=Ref(vpcnametag)
                )
            ))

routetablepublic = t.add_resource(RouteTable(
            "RouteTablePublic",
            VpcId=Ref(vpc),
            Tags=Tags(
                Name=Ref(routetablepublicname)
                )
            ))

routetableprivate = t.add_resource(RouteTable(
            "RouteTablePrivate",
            VpcId=Ref(vpc),
            Tags=Tags(
                Name=Ref(routetableprivatename)
                )
            ))

networkaclpublic = t.add_resource(NetworkAcl(
            "NetworkAclPublic",
            VpcId=Ref(vpc),
            Tags=Tags(
                Name=Ref(networkaclpublicname)
                )
            ))

networkaclprivate = t.add_resource(NetworkAcl(
            "NetworkAclPrivate",
            VpcId=Ref(vpc),
            Tags=Tags(
                Name=Ref(networkaclprivatename)
                )
            ))

internetgateway = t.add_resource(InternetGateway(
            "InternetGateway",
            Tags=Tags(
                Name=Ref(internetgatewayname)
                )
            ))

vpcigattach = t.add_resource(VPCGatewayAttachment(
            "VPCtoIG",
            InternetGatewayId=Ref(internetgateway),
            VpcId=Ref(vpc)
            ))

subnetpublic1 = t.add_resource(Subnet(
            "SubnetPublic1",
            CidrBlock=Ref(subnetcidrpublic1),
            MapPublicIpOnLaunch="true",
            VpcId=Ref(vpc),
            Tags=Tags(
                Name=Ref(subnetpublic1name)
                )
            ))

subnetpublic2 = t.add_resource(Subnet(
            "SubnetPublic2",
            CidrBlock=Ref(subnetcidrpublic2),
            MapPublicIpOnLaunch="true",
            VpcId=Ref(vpc),
            Tags=Tags(
                Name=Ref(subnetpublic2name)
                )
            ))

subnetprivate1 = t.add_resource(Subnet(
            "SubnetPrivate1",
            CidrBlock=Ref(subnetcidrprivate1),
            VpcId=Ref(vpc),
            Tags=Tags(
                Name=Ref(subnetprivate1name)
                )
            ))

subnetprivate2 = t.add_resource(Subnet(
            "SubnetPrivate2",
            CidrBlock=Ref(subnetcidrprivate2),
            VpcId=Ref(vpc),
            Tags=Tags(
                Name=Ref(subnetprivate2name)
                )
            ))

public1subnetaclassoc = t.add_resource(SubnetNetworkAclAssociation(
            "Public1SubnetAclAssociation",
            SubnetId=Ref(subnetpublic1),
            NetworkAclId=Ref(networkaclpublic)
            ))

public2subnetaclassoc = t.add_resource(SubnetNetworkAclAssociation(
            "Public2SubnetAclAssociation",
            SubnetId=Ref(subnetpublic2),
            NetworkAclId=Ref(networkaclpublic)
            ))

private1subnetaclassoc = t.add_resource(SubnetNetworkAclAssociation(
            "Private1SubnetAclAssociation",
            SubnetId=Ref(subnetprivate1),
            NetworkAclId=Ref(networkaclprivate)
            ))

private2subnetaclassoc = t.add_resource(SubnetNetworkAclAssociation(
            "Private2SubnetAclAssociation",
            SubnetId=Ref(subnetprivate2),
            NetworkAclId=Ref(networkaclprivate)
            ))

elasticip = t.add_resource(EIP(
            "NatElasticIP"
            ))

public1natgateway = t.add_resource(NatGateway(
            "NatGatewayPublic1",
            AllocationId=GetAtt(elasticip, "AllocationId"),
            SubnetId=Ref(subnetpublic1),
            Tags=Tags(
                Name=Ref(natgatewayname)
                )
            ))

publicroute = t.add_resource(Route(
            "PublicRoute",
            DestinationCidrBlock="0.0.0.0/0",
            GatewayId=Ref(internetgateway),
            RouteTableId=Ref(routetablepublic)
            ))

privateroute = t.add_resource(Route(
            "PrivateRoute",
            DestinationCidrBlock="0.0.0.0/0",
            NatGatewayId=Ref(public1natgateway),
            RouteTableId=Ref(routetableprivate)
            ))

subnetroutetablepublic1assoc = t.add_resource(SubnetRouteTableAssociation(
            "SubnetRoutetablePublic1Assoc",
            RouteTableId=Ref(routetablepublic),
            SubnetId=Ref(subnetpublic1)
            ))

subnetroutetablepublic2assoc = t.add_resource(SubnetRouteTableAssociation(
            "SubnetRoutetablePublic2Assoc",
            RouteTableId=Ref(routetablepublic),
            SubnetId=Ref(subnetpublic2)
            ))

subnetroutetableprivate1assoc = t.add_resource(SubnetRouteTableAssociation(
            "SubnetRoutetablePrivate1Assoc",
            RouteTableId=Ref(routetableprivate),
            SubnetId=Ref(subnetprivate1)
            ))

subnetroutetableprivate2assoc = t.add_resource(SubnetRouteTableAssociation(
            "SubnetRoutetablePrivate2Assoc",
            RouteTableId=Ref(routetableprivate),
            SubnetId=Ref(subnetprivate2)
            ))

t.add_output([
    Output(
        "VpcId",
        Description="Newly Created Vpc Id",
        Value=Ref(vpc)
    ),
    Output(
        "PublicRoutable",
        Description="Newly Created Public Roubtable",
        Value=Ref(routetablepublic)
    ),
    Output(
        "PrivateRoutable",
        Description="Newly Created Private Roubtable",
        Value=Ref(routetableprivate)
    ),
    Output(
        "PublicNetworkACL",
        Description="Newly Created Public NetworkAcl",
        Value=Ref(networkaclpublic)
    ),
    Output(
        "PrivateNetworkACL",
        Description="Newly Created Private NetworkAcl",
        Value=Ref(networkaclprivate)
    ),
    Output(
        "InternetGateway",
        Description="Newly Created Internet Gateway",
        Value=Ref(internetgateway)
    ),
    Output(
        "PublicSubnet1",
        Description="Newly Created Public Subnet 1",
        Value=Ref(subnetpublic1)
    ),
    Output(
        "PublicSubnet2",
        Description="Newly Created Public Subnet 2",
        Value=Ref(subnetpublic2)
    ),
    Output(
        "PrivateSubnet1",
        Description="Newly Created Private Subnet 1",
        Value=Ref(subnetprivate1)
    ),
    Output(
        "PrivateSubnet2",
        Description="Newly Created Private Subnet 2",
        Value=Ref(subnetprivate2)
    ),
    Output(
        "NatGatewayId",
        Description="Newly Created NatGateway",
        Value=Ref(public1natgateway)
    )
])

print(t.to_json())
