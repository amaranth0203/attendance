/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2017/7/20 20:23:12                           */
/*==============================================================*/


drop table if exists attendance._class_teacher_to_building;

drop table if exists attendance._class_teacher_to_dormitory;

drop table if exists attendance._class_to_building;

drop table if exists attendance._class_to_dormitory;

drop table if exists attendance._dormitory_to_building;

drop table if exists attendance.building;

drop table if exists attendance.class;

drop table if exists attendance.class_teacher;

drop table if exists attendance.dormitory;

drop table if exists attendance.photos;

drop table if exists attendance.position;

drop table if exists attendance.student;

drop table if exists attendance.user;

drop table if exists attendance.wechat;

/*==============================================================*/
/* Table: _class_teacher_to_building                            */
/*==============================================================*/
create table attendance._class_teacher_to_building
(
   class_teacher_id     bigint not null,
   building_id          bigint not null,
   primary key (class_teacher_id, building_id)
);

/*==============================================================*/
/* Table: _class_teacher_to_dormitory                           */
/*==============================================================*/
create table attendance._class_teacher_to_dormitory
(
   class_teacher_id     bigint not null,
   dormitory_id         bigint not null,
   primary key (class_teacher_id, dormitory_id)
);

/*==============================================================*/
/* Table: _class_to_building                                    */
/*==============================================================*/
create table attendance._class_to_building
(
   class_id             bigint not null,
   building_id          bigint not null,
   primary key (class_id, building_id)
);

/*==============================================================*/
/* Table: _class_to_dormitory                                   */
/*==============================================================*/
create table attendance._class_to_dormitory
(
   class_id             bigint not null,
   dormitory_id         bigint not null,
   primary key (class_id, dormitory_id)
);

/*==============================================================*/
/* Table: _dormitory_to_building                                */
/*==============================================================*/
create table attendance._dormitory_to_building
(
   dormitory_id         bigint not null,
   building_id          bigint not null,
   primary key (dormitory_id, building_id)
);

/*==============================================================*/
/* Table: building                                              */
/*==============================================================*/
create table attendance.building
(
   id                   bigint not null auto_increment,
   name                 varchar(128),
   primary key (id)
);

/*==============================================================*/
/* Table: class                                                 */
/*==============================================================*/
create table attendance.class
(
   id                   bigint not null auto_increment,
   name                 varchar(128),
   class_teacher_id     bigint,
   primary key (id)
);

/*==============================================================*/
/* Table: class_teacher                                         */
/*==============================================================*/
create table attendance.class_teacher
(
   id                   bigint not null auto_increment,
   name                 varchar(128),
   cellphone            varchar(128),
   number               varchar(128),
   user_id              bigint,
   primary key (id),
   unique key UNI_class_teacher_fk_to_user (user_id)
);

/*==============================================================*/
/* Table: dormitory                                             */
/*==============================================================*/
create table attendance.dormitory
(
   id                   bigint not null auto_increment,
   name                 varchar(128),
   building_id          bigint,
   primary key (id)
);

/*==============================================================*/
/* Table: photos                                                */
/*==============================================================*/
create table attendance.photos
(
   id                   bigint not null auto_increment,
   content              binary(0),
   time                 timestamp,
   wechat_id            bigint,
   primary key (id)
);

/*==============================================================*/
/* Table: position                                              */
/*==============================================================*/
create table attendance.position
(
   id                   bigint not null auto_increment,
   time                 timestamp,
   accuracy             double,
   longitude            double,
   latitude             double,
   wechat_id            bigint,
   primary key (id)
);

/*==============================================================*/
/* Table: student                                               */
/*==============================================================*/
create table attendance.student
(
   id                   bigint not null auto_increment,
   name                 varchar(128),
   cellphone            varchar(128),
   student_number       varchar(128),
   non_resident         boolean,
   class_teacher_id     bigint,
   dormitory_id         bigint,
   class_id             bigint,
   building_id          bigint,
   user_id              bigint,
   primary key (id)
);

/*==============================================================*/
/* Table: user                                                  */
/*==============================================================*/
create table attendance.user
(
   id                   bigint not null auto_increment,
   username             varchar(128),
   password             varchar(128),
   primary key (id)
);

/*==============================================================*/
/* Table: wechat                                                */
/*==============================================================*/
create table attendance.wechat
(
   id                   bigint not null auto_increment,
   nickname             varchar(128),
   openid               varchar(128),
   user_id              bigint,
   primary key (id)
);

alter table attendance._class_teacher_to_building add constraint FK_fk_cttb_to_building foreign key (building_id)
      references attendance.building (id) on delete restrict on update restrict;

alter table attendance._class_teacher_to_building add constraint FK_fk_cttb_to_class_teacher foreign key (class_teacher_id)
      references attendance.class_teacher (id) on delete restrict on update restrict;

alter table attendance._class_teacher_to_dormitory add constraint FK_fk_cttd_to_class_teacher foreign key (class_teacher_id)
      references attendance.class_teacher (id) on delete restrict on update restrict;

alter table attendance._class_teacher_to_dormitory add constraint FK_fk_cttd_to_dormitory foreign key (dormitory_id)
      references attendance.dormitory (id) on delete restrict on update restrict;

alter table attendance._class_to_building add constraint FK_fk_ctb_to_building_id foreign key (building_id)
      references attendance.building (id) on delete restrict on update restrict;

alter table attendance._class_to_building add constraint FK_fk_ctb_to_class_id foreign key (class_id)
      references attendance.class (id) on delete restrict on update restrict;

alter table attendance._class_to_dormitory add constraint FK_fk_ctd__to_class_id foreign key (class_id)
      references attendance.class (id) on delete restrict on update restrict;

alter table attendance._class_to_dormitory add constraint FK_fk_ctd_to_dormitory_id foreign key (dormitory_id)
      references attendance.dormitory (id) on delete restrict on update restrict;

alter table attendance._dormitory_to_building add constraint FK_fd_dtb_to_building_id foreign key (building_id)
      references attendance.building (id) on delete restrict on update restrict;

alter table attendance._dormitory_to_building add constraint FK_fk_dtb_to_dormitory_id foreign key (dormitory_id)
      references attendance.dormitory (id) on delete restrict on update restrict;

alter table attendance.class add constraint FK_fk_class_to_class_teacher_id foreign key (class_teacher_id)
      references attendance.class_teacher (id) on delete restrict on update restrict;

alter table attendance.class_teacher add constraint FK_fk_class_teacher_to_user foreign key (user_id)
      references attendance.user (id) on delete restrict on update restrict;

alter table attendance.photos add constraint FK_fk_photos_to_wechat_id foreign key (wechat_id)
      references attendance.wechat (id) on delete restrict on update restrict;

alter table attendance.position add constraint FK_fk_position_to_wechat_id foreign key (wechat_id)
      references attendance.wechat (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_building_id foreign key (building_id)
      references attendance.building (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_class_id foreign key (class_id)
      references attendance.class (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_class_teacher_id foreign key (class_teacher_id)
      references attendance.class_teacher (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_dormitory_id foreign key (dormitory_id)
      references attendance.dormitory (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_user_id foreign key (user_id)
      references attendance.user (id) on delete restrict on update restrict;

alter table attendance.wechat add constraint FK_fk_wechat_to_user_id foreign key (user_id)
      references attendance.user (id) on delete restrict on update restrict;

