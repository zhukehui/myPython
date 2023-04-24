CREATE TABLE `calculation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '名称',
  `electric_quantity` int(100) NOT NULL COMMENT '电量（°）',
  `used_electricity` int(50) DEFAULT NULL COMMENT '已用电量（°）',
  `unit_price` varchar(20) DEFAULT NULL,
  `amount` varchar(20) NOT NULL COMMENT '电费 单位:分',
  `date_calculation` varchar(50) NOT NULL COMMENT '计算日期',
  `deleted` bigint(1) DEFAULT '0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
)  COMMENT='历史电费记录表';

INSERT INTO `calculation` (`name`, `electric_quantity`, `used_electricity`, `unit_price`, `amount`, `date_calculation`) 
VALUES 
('①', 1664, 239, '0.81381', '194.50059', '2023-01'),
('②', 3610, 264, '0.81381', '214.84584', '2023-01'),
('③', 2550, 250, '0.81381', '203.45250', '2023-01'),
('①', 1816, 152, '0.52173', '79.30296', '2023-02'),
('②', 3785, 113, '0.52173', '91.30275', '2023-02'),
('③', 2675, 56, '0.52173', '88.69410', '2023-02'),
('①', 1911, 96, '0.63861', '54.70176', '2023-03'),
('②', 4069, 113, '0.63861', '64.38853', '2023-03'),
('③', 2814, 56, '0.63861', '31.90936', '2023-03'),
('①', 2007, 96, '0.56981', '54.70176', '2023-04'),
('②', 4182, 113, '0.56981', '64.38853', '2023-04'),
('③', 2870, 56, '0.56981', '31.90936', '2023-04');