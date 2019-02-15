# -*- coding: utf-8 -*-

from oslo_config import cfg

MYCONF = cfg.CONF

# 指定配置文件
MYCONF(default_config_files=['/root/code/zhuangshi/geml.conf']) 

# 默认参数注册
# [DEFAULT] common_opts 参数，全部在 DEFAULT 组下面
 
common_opts = [
    cfg.StrOpt('bind_host',
               default='0.0.0.0',
               help='IP address to listen on.'),
    cfg.Opt('bind_port',
            default=9292,
            help='Port number to listen on.'),
    cfg.ListOpt('enable_cells', default=[])
]
# 注册
MYCONF.register_opts(common_opts)


# 注册一个 section
# section 注册分两个步骤
# 1 名字注册
# 2 section 中参数注册
 
def registrey_cell(MYCONF, group_name):

    # 注册service组group
    service_opt_group = cfg.OptGroup(
							name=group_name,
							title='The service which use the scheduler'
						)
    MYCONF.register_group(service_opt_group)
    # 注册group 包含                                           
    #注册属于service_opts组的配置选项，用了StrOpt、IntOpt和IPOpt的参数
    service_opts = [
            cfg.StrOpt('service',
                       default='sora_compute',
                       help='The default user service'),
            cfg.IntOpt('service_id',
                       default=1,
                       help='The service id'),
            cfg.IPOpt('endpoint_ip',
                       help='The service endpoint ip'),
    ]
    # 把参数注册到组中
    MYCONF.register_opts(service_opts, group=service_opt_group)
    # section的获得
    print MYCONF.get(group_name).service
    print MYCONF.get(group_name).service
    print MYCONF.get(group_name).service_id


if __name__ == "__main__":
    cells = MYCONF.enable_cells
    for cell in cells:
        print(cell)
        registrey_cell(MYCONF, cell)
