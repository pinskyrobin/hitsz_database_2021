/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/11/17 14:07:49                          */
/*==============================================================*/


/*==============================================================*/
/* Table: admin                                                 */
/*==============================================================*/
create table admin
(
   admin_id             int not null,
   admin_name           varchar(16) not null,
   admin_psw            varchar(256) not null,
   store_access         int not null,
   canteen_access       int not null,
   primary key (admin_id)
);

/*==============================================================*/
/* Table: canteen                                               */
/*==============================================================*/
create table canteen
(
   canteen_id           int not null,
   canteen_name         varchar(16) not null,
   canteen_pic          varchar(128),
   canteen_status       bool,
   primary key (canteen_id)
);

/*==============================================================*/
/* Index: canteen_name_UNIQUE                                   */
/*==============================================================*/
create unique index canteen_name_UNIQUE on canteen
(
   canteen_name
);

/*==============================================================*/
/* Table: cmt                                                   */
/*==============================================================*/
create table cmt
(
   comment_id           int not null,
   order_id             int not null,
   comment_content      varchar(512),
   comment_level        int not null,
   comment_time         timestamp not null,
   primary key (comment_id)
);

/*==============================================================*/
/* Table: orders                                                */
/*==============================================================*/
create table orders
(
   order_id             int not null,
   user_id              int not null,
   store_id             int not null,
   total                decimal(4,1) not null,
   order_status         int not null,
   create_time          timestamp not null,
   modified_time        timestamp not null,
   primary key (order_id)
);

/*==============================================================*/
/* Table: prd_order                                             */
/*==============================================================*/
create table prd_order
(
   order_id             int not null,
   prd_id               int not null,
   primary key (order_id, prd_id)
);

/*==============================================================*/
/* Table: product                                               */
/*==============================================================*/
create table product
(
   prd_id               int not null,
   prd_name             varchar(16) not null,
   prd_intro            varchar(128),
   prd_price            numeric(4,1) not null,
   store_id             int not null,
   prd_amount           int not null,
   prd_status           int not null,
   primary key (prd_id)
);

/*==============================================================*/
/* Table: store                                                 */
/*==============================================================*/
create table store
(
   store_id             int not null,
   store_name           varchar(32) not null,
   canteen_id           int not null,
   store_floor          int not null,
   primary key (store_id)
);

/*==============================================================*/
/* Index: store_name_UNIQUE                                     */
/*==============================================================*/
create unique index store_name_UNIQUE on store
(
   store_name
);

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users
(
   user_id              int not null,
   user_name            varchar(16) not null,
   user_psw             varchar(256) not null,
   primary key (user_id)
);

/*==============================================================*/
/* View: canteen_info                                           */
/*==============================================================*/
create
VIEW

canteen_info as
select `canteen`.`canteen_id` AS `canteen_id`,
        `store`.`store_id` AS `store_id`,
        concat(`store`.`store_floor`,'楼: ',`store`.`store_name`) AS `loc`,
        `cmt`.`comment_level` AS `comment_level`,
        `cmt`.`comment_content` AS `comment_content`,
        `cmt`.`comment_time` AS `comment_time` 
from cmt, orders, store, canteen 
where ((`cmt`.`order_id` = `orders`.`order_id`) 
        and (`orders`.`store_id` = `store`.`store_id`) 
        and (`store`.`canteen_id` = `canteen`.`canteen_id`)) 
order by `cmt`.`comment_time` desc;

alter table cmt add constraint FK_order_comment foreign key (order_id)
      references orders (order_id) on delete restrict on update restrict;

alter table orders add constraint FK_order_user foreign key (user_id)
      references users (user_id) on delete restrict on update restrict;

alter table orders add constraint FK_store_order foreign key (store_id)
      references store (store_id) on delete restrict on update restrict;

alter table prd_order add constraint FK_prd_order foreign key (order_id)
      references orders (order_id) on delete restrict on update restrict;

alter table prd_order add constraint FK_prd_order2 foreign key (prd_id)
      references product (prd_id) on delete restrict on update restrict;

alter table product add constraint FK_store_prd foreign key (store_id)
      references store (store_id) on delete restrict on update restrict;

alter table store add constraint FK_canteen_store foreign key (canteen_id)
      references canteen (canteen_id) on delete restrict on update restrict;


CREATE TRIGGER `order_before_update` 
BEFORE UPDATE ON `orders` 
FOR EACH ROW update product
        set product.prd_amount=product.prd_amount+1
        where prd_id in (
            select prd_id
                        from prd_order, orders
                        where orders.order_id = old.order_id
            and orders.order_id = prd_order.order_id
        );

select `canteen`.`canteen_id` AS `canteen_id`,
        `store`.`store_id` AS `store_id`,
        concat(`store`.`store_floor`,'楼: ',`store`.`store_name`) AS `loc`,
        `cmt`.`comment_level` AS `comment_level`,
        `cmt`.`comment_content` AS `comment_content`,
        `cmt`.`comment_time` AS `comment_time` 
from cmt, orders, store, canteen 
where ((`cmt`.`order_id` = `orders`.`order_id`) 
        and (`orders`.`store_id` = `store`.`store_id`) 
        and (`store`.`canteen_id` = `canteen`.`canteen_id`)) 
order by `cmt`.`comment_time` desc;

