/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2017/7/21 21:19:13                           */
/*==============================================================*/


drop table if exists attendance._claxx_teacher_to_building;

drop table if exists attendance._claxx_teacher_to_dormitory;

drop table if exists attendance._claxx_to_building;

drop table if exists attendance._claxx_to_dormitory;

drop table if exists attendance.building;

drop table if exists attendance.claxx;

drop table if exists attendance.claxx_teacher;

drop table if exists attendance.dormitory;

drop table if exists attendance.photos;

drop table if exists attendance.position;

drop table if exists attendance.student;

drop table if exists attendance.user;

drop table if exists attendance.wechat;

/*==============================================================*/
/* Table: _claxx_teacher_to_building                            */
/*==============================================================*/
create table attendance._claxx_teacher_to_building
(
   claxx_teacher_id     bigint not null,
   building_id          bigint not null,
   primary key (claxx_teacher_id, building_id)
);

/*==============================================================*/
/* Table: _claxx_teacher_to_dormitory                           */
/*==============================================================*/
create table attendance._claxx_teacher_to_dormitory
(
   claxx_teacher_id     bigint not null,
   dormitory_id         bigint not null,
   primary key (claxx_teacher_id, dormitory_id)
);

/*==============================================================*/
/* Table: _claxx_to_building                                    */
/*==============================================================*/
create table attendance._claxx_to_building
(
   claxx_id             bigint not null,
   building_id          bigint not null,
   primary key (claxx_id, building_id)
);

/*==============================================================*/
/* Table: _claxx_to_dormitory                                   */
/*==============================================================*/
create table attendance._claxx_to_dormitory
(
   claxx_id             bigint not null,
   dormitory_id         bigint not null,
   primary key (claxx_id, dormitory_id)
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
/* Table: claxx                                                 */
/*==============================================================*/
create table attendance.claxx
(
   id                   bigint not null auto_increment,
   name                 varchar(128),
   claxx_teacher_id     bigint,
   primary key (id)
);

/*==============================================================*/
/* Table: claxx_teacher                                         */
/*==============================================================*/
create table attendance.claxx_teacher
(
   id                   bigint not null auto_increment,
   name                 varchar(128),
   cellphone            varchar(128),
   number               varchar(128),
   user_id              bigint,
   primary key (id),
   unique key UNI_claxx_teacher_fk_to_user (user_id)
);

/*==============================================================*/
/* Table: dormitory                                             */
/*==============================================================*/
create table attendance.dormitory
(
   id                   bigint not null,
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
   claxx_teacher_id     bigint,
   dormitory_id         bigint,
   claxx_id             bigint,
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

alter table attendance._claxx_teacher_to_building add constraint FK_fk_cttb_to_building foreign key (building_id)
      references attendance.building (id) on delete restrict on update restrict;

alter table attendance._claxx_teacher_to_building add constraint FK_fk_cttb_to_claxx_teacher foreign key (claxx_teacher_id)
      references attendance.claxx_teacher (id) on delete restrict on update restrict;

alter table attendance._claxx_teacher_to_dormitory add constraint FK_fk_cttd_to_claxx_teacher foreign key (claxx_teacher_id)
      references attendance.claxx_teacher (id) on delete restrict on update restrict;

alter table attendance._claxx_teacher_to_dormitory add constraint FK_fk_cttd_to_dormitory foreign key (dormitory_id)
      references attendance.dormitory (id) on delete restrict on update restrict;

alter table attendance._claxx_to_building add constraint FK_fk_ctb_to_building_id foreign key (building_id)
      references attendance.building (id) on delete restrict on update restrict;

alter table attendance._claxx_to_building add constraint FK_fk_ctb_to_claxx_id foreign key (claxx_id)
      references attendance.claxx (id) on delete restrict on update restrict;

alter table attendance._claxx_to_dormitory add constraint FK_fk_ctd_to_claxx_id foreign key (claxx_id)
      references attendance.claxx (id) on delete restrict on update restrict;

alter table attendance._claxx_to_dormitory add constraint FK_fk_ctd_to_dormitory_id foreign key (dormitory_id)
      references attendance.dormitory (id) on delete restrict on update restrict;

alter table attendance.claxx add constraint FK_fk_claxx_to_claxx_teacher_id foreign key (claxx_teacher_id)
      references attendance.claxx_teacher (id) on delete restrict on update restrict;

alter table attendance.claxx_teacher add constraint FK_fk_claxx_teacher_to_user foreign key (user_id)
      references attendance.user (id) on delete restrict on update restrict;

alter table attendance.dormitory add constraint FK_fk_dormtory_to_building foreign key (building_id)
      references attendance.building (id) on delete restrict on update restrict;

alter table attendance.photos add constraint FK_fk_photos_to_wechat_id foreign key (wechat_id)
      references attendance.wechat (id) on delete restrict on update restrict;

alter table attendance.position add constraint FK_fk_position_to_wechat_id foreign key (wechat_id)
      references attendance.wechat (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_building_id foreign key (building_id)
      references attendance.building (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_claxx_id foreign key (claxx_id)
      references attendance.claxx (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_claxx_teacher_id foreign key (claxx_teacher_id)
      references attendance.claxx_teacher (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_dormitory_id foreign key (dormitory_id)
      references attendance.dormitory (id) on delete restrict on update restrict;

alter table attendance.student add constraint FK_fk_student_to_user_id foreign key (user_id)
      references attendance.user (id) on delete restrict on update restrict;

alter table attendance.wechat add constraint FK_fk_wechat_to_user_id foreign key (user_id)
      references attendance.user (id) on delete restrict on update restrict;

