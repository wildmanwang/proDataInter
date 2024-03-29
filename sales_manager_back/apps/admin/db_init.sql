-- 应用
insert into sysapp ( name, order_number, status ) values ( "商家后台", 10, 1 );
insert into sysapp ( name, order_number, status ) values ( "销售前台", 20, 1 );
insert into sysapp ( name, order_number, status ) values ( "用户端", 30, 1 );

-- 模块
insert into sysmodel ( name, sysapp, code, icon, order_number, status, remark ) values ( "用户中心", 1, 'user', 'el-icon-user-solid', 10, 1, '组织结构、用户管理、权限管理' );
insert into sysmodel ( name, sysapp, code, icon, order_number, status, remark ) values ( "商品管理", 1, 'goods', 'el-icon-s-goods', 20, 1, '商品维修' );
insert into sysmodel ( name, sysapp, code, icon, order_number, status, remark ) values ( "订单管理", 1, 'order', 'el-icon-s-order', 30, 1, '订单流程管理' );
insert into sysmodel ( name, sysapp, code, icon, order_number, status, remark ) values ( "采购管理", 1, 'purchase', 'el-icon-s-platform', 40, 1, '采购流程管理' );
insert into sysmodel ( name, sysapp, code, icon, order_number, status, remark ) values ( "仓库管理", 1, 'store', 'el-icon-s-home', 50, 1, '仓库流程管理' );

-- 功能
insert into sysfunction ( name, sysmodel, authorizate_flag, code, icon, order_number, status ) values ( '角色管理', 1, 1, 'role', 'el-icon-coordinate', 10, 1 );
insert into sysfunction ( name, sysmodel, authorizate_flag, code, icon, order_number, status ) values ( '用户管理', 1, 1, 'user', 'el-icon-user', 20, 1 );
insert into sysfunction ( name, sysmodel, authorizate_flag, code, icon, order_number, status ) values ( '组织管理', 1, 1, 'organize', 'el-icon-office-building', 30, 1 );
insert into sysfunction ( name, sysmodel, authorizate_flag, code, icon, order_number, status ) values ( '部门管理', 1, 1, 'department', 'el-icon-suitcase', 40, 1 );
insert into sysfunction ( name, sysmodel, authorizate_flag, code, icon, order_number, status ) values ( '员工管理', 1, 1, 'staff', 'el-icon-table-lamp', 50, 1 );
insert into sysfunction ( name, sysmodel, authorizate_flag, code, icon, order_number, status ) values ( '商品类别', 2, 1, 'category', 'el-icon-folder', 10, 1 );
insert into sysfunction ( name, sysmodel, authorizate_flag, code, icon, order_number, status ) values ( '供应商', 2, 1, 'supplier', 'el-icon-truck', 20, 1 );
insert into sysfunction ( name, sysmodel, authorizate_flag, code, icon, order_number, status ) values ( '商品管理', 2, 1, 'goods', 'el-icon-goods', 30, 1 );

-- 操作
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '查看', 1, 10, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '新增', 1, 20, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '修改', 1, 30, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '禁用', 1, 40, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '删除', 1, 50, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '配置权限', 1, 60, 1 );

insert into sysoperation ( name, sysfunction, order_number, status ) values ( '新增', 2, 10, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '修改', 2, 20, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '禁用', 2, 30, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '授权', 2, 40, 1 );

insert into sysoperation ( name, sysfunction, order_number, status ) values ( '新增', 3, 10, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '修改', 3, 20, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '禁用', 3, 30, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '删除', 3, 40, 1 );

insert into sysoperation ( name, sysfunction, order_number, status ) values ( '新增', 4, 10, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '修改', 4, 20, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '禁用', 4, 30, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '删除', 4, 40, 1 );

insert into sysoperation ( name, sysfunction, order_number, status ) values ( '新增', 5, 10, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '修改', 5, 20, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '转正', 5, 30, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '离职', 5, 40, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '删除', 5, 50, 1 );

insert into sysoperation ( name, sysfunction, order_number, status ) values ( '新增', 6, 10, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '修改', 6, 20, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '禁用', 6, 30, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '删除', 6, 40, 1 );

insert into sysoperation ( name, sysfunction, order_number, status ) values ( '新增', 7, 10, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '修改', 7, 20, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '禁用', 7, 30, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '删除', 7, 40, 1 );

insert into sysoperation ( name, sysfunction, order_number, status ) values ( '新增', 8, 10, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '修改', 8, 20, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '禁用', 8, 30, 1 );
insert into sysoperation ( name, sysfunction, order_number, status ) values ( '删除', 8, 40, 1 );

-- 角色
insert into sysrole ( name, order_number, status ) values ( '超级管理员', 10, 1 );

-- 组织
insert into organization ( name, simple_name, order_number, status ) values ( '石将军智能家居', '石将军', 10, 1 );
