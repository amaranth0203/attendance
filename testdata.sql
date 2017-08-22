delete from _claxx_to_building;

delete from _claxx_to_dormitory;

delete from student;

delete from claxx;

delete from _claxx_teacher_to_building;

delete from _claxx_teacher_to_dormitory;

delete from claxx_teacher;

delete from user;

delete from dormitory;

delete from building;

insert into building (id, name) values (1, '住宿楼1');
insert into building (id, name) values (2, '住宿楼2');

insert into dormitory (id, name, building_id) values (1, '宿舍1', 1);
insert into dormitory (id, name, building_id) values (2, '宿舍2', 1);
insert into dormitory (id, name, building_id) values (3, '宿舍3', 2); -- 混住
insert into dormitory (id, name, building_id) values (4, '宿舍4', 2);

insert into user (id, username, password) values (1, 'gxxd001', '123456');
insert into user (id, username, password) values (2, 'gxxd002', '123456');
insert into user (id, username, password) values (3, 'gxxd_stu1', '123456');
insert into user (id, username, password) values (4, 'gxxd_stu2', '123456');
insert into user (id, username, password) values (5, 'gxxd_stu3', '123456');
insert into user (id, username, password) values (6, 'gxxd_stu4', '123456');
insert into user (id, username, password) values (7, 'gxxd_stu5', '123456');
insert into user (id, username, password) values (8, 'gxxd_stu6', '123456');
insert into user (id, username, password) values (9, 'gxxd_stu7', '123456');
insert into user (id, username, password) values (10, 'gxxd_stu8', '123456');
insert into user (id, username, password) values (11, 'gxxd_stu9', '123456');

insert into claxx_teacher (id, name, cellphone, number, user_id) values (1, '班主任1', '13132780001', 'gxxd001', 1);
insert into claxx_teacher (id, name, cellphone, number, user_id) values (2, '班主任2', '13132780002', 'gxxd002', 2);

insert into _claxx_teacher_to_dormitory (claxx_teacher_id, number, dormitory_id) values (1, 'gxxd001', 1);
insert into _claxx_teacher_to_dormitory (claxx_teacher_id, number, dormitory_id) values (1, 'gxxd001', 2);
insert into _claxx_teacher_to_dormitory (claxx_teacher_id, number, dormitory_id) values (1, 'gxxd001', 3);
insert into _claxx_teacher_to_dormitory (claxx_teacher_id, number, dormitory_id) values (2, 'gxxd002', 3);
insert into _claxx_teacher_to_dormitory (claxx_teacher_id, number, dormitory_id) values (2, 'gxxd002', 4);

insert into _claxx_teacher_to_building (claxx_teacher_id, number, building_id) values (1, 'gxxd001', 1);
insert into _claxx_teacher_to_building (claxx_teacher_id, number, building_id) values (1, 'gxxd001', 2);
insert into _claxx_teacher_to_building (claxx_teacher_id, number, building_id) values (2, 'gxxd002', 2);

insert into claxx (id, name, claxx_teacher_id) values (1, '机械1班', 1);
insert into claxx (id, name, claxx_teacher_id) values (2, '机械2班', 2);

insert into _claxx_to_dormitory (claxx_id, dormitory_id) values (1, 1);
insert into _claxx_to_dormitory (claxx_id, dormitory_id) values (1, 2);
insert into _claxx_to_dormitory (claxx_id, dormitory_id) values (1, 3);
insert into _claxx_to_dormitory (claxx_id, dormitory_id) values (2, 3);
insert into _claxx_to_dormitory (claxx_id, dormitory_id) values (2, 4);

insert into _claxx_to_building (claxx_id, building_id) values (1, 1);
insert into _claxx_to_building (claxx_id, building_id) values (1, 2);
insert into _claxx_to_building (claxx_id, building_id) values (2, 2);

insert into student (id, name, cellphone, student_number, non_resident, claxx_teacher_id, number, dormitory_id, claxx_id, building_id, user_id) values (1, '一班学生1', '13132780901', 'gxxd_stu1', 0, 1, 'gxxd001', 1, 1, 1, 3);
insert into student (id, name, cellphone, student_number, non_resident, claxx_teacher_id, number, dormitory_id, claxx_id, building_id, user_id) values (2, '一班学生2', '13132780902', 'gxxd_stu2', 0, 1, 'gxxd001', 1, 1, 1, 4);
insert into student (id, name, cellphone, student_number, non_resident, claxx_teacher_id, number, dormitory_id, claxx_id, building_id, user_id) values (3, '一班学生3', '13132780903', 'gxxd_stu3', 0, 1, 'gxxd001', 2, 1, 1, 5);
insert into student (id, name, cellphone, student_number, non_resident, claxx_teacher_id, number, dormitory_id, claxx_id, building_id, user_id) values (4, '一班学生4', '13132780904', 'gxxd_stu4', 0, 1, 'gxxd001', 2, 1, 1, 6);
insert into student (id, name, cellphone, student_number, non_resident, claxx_teacher_id, number, dormitory_id, claxx_id, building_id, user_id) values (5, '一班学生5', '13132780905', 'gxxd_stu5', 0, 1, 'gxxd001', 3, 1, 2, 7);
insert into student (id, name, cellphone, student_number, non_resident, claxx_teacher_id, number, dormitory_id, claxx_id, building_id, user_id) values (6, '二班学生2', '13132780906', 'gxxd_stu6', 0, 2, 'gxxd002', 3, 2, 2, 8);
insert into student (id, name, cellphone, student_number, non_resident, claxx_teacher_id, number, dormitory_id, claxx_id, building_id, user_id) values (7, '二班学生3', '13132780907', 'gxxd_stu7', 0, 2, 'gxxd002', 4, 2, 2, 9);
insert into student (id, name, cellphone, student_number, non_resident, claxx_teacher_id, number, dormitory_id, claxx_id, building_id, user_id) values (8, '二班学生4', '13132780908', 'gxxd_stu8', 0, 2, 'gxxd002', 4, 2, 2, 10);
insert into student (id, name, cellphone, student_number, non_resident, claxx_teacher_id, number, dormitory_id, claxx_id, building_id, user_id) values (9, '二班学生5', '13132780909', 'gxxd_stu9', 1, 2, 'gxxd002', null, 2, null, 11);
