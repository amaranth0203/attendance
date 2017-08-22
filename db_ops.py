
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

import urllib.request
import json

engine = create_engine( 'mysql+pymysql://attendance:echo@localhost/attendance?charset=utf8' , echo=False , encoding='utf-8' )
metadata = MetaData( engine )
Base = declarative_base( )
Base.metadata = metadata
session = sessionmaker( engine )( )

class _claxx_teacher_to_building( Base ) :
    def __init__(self, outer):
        self.outer = outer
    __table__ = Table( '_claxx_teacher_to_building' , metadata , autoload = True )
    claxx_teacher = relationship( 'claxx_teacher' , back_populates = 'buildings' )
    building = relationship( "building" , back_populates = "claxx_teachers" )
class _claxx_teacher_to_dormitory( Base ) :
    __table__ = Table( '_claxx_teacher_to_dormitory' , metadata , autoload = True )
    claxx_teacher = relationship( 'claxx_teacher' , back_populates = 'dormitories' )
    dormitory = relationship( 'dormitory' , back_populates = 'claxx_teachers' )
class _claxx_to_dormitory( Base ) :
    __table__ = Table( '_claxx_to_dormitory' , metadata , autoload = True )
    dormitory = relationship( "dormitory" , back_populates = "claxxes" )
    claxx = relationship( "claxx" , back_populates = "dormitories" )
class _claxx_to_building( Base ) :
    __table__ = Table( '_claxx_to_building' , metadata , autoload = True )
    building = relationship( "building" , back_populates = "claxxes" )
    claxx = relationship( "claxx" , back_populates = "buildings" )

class wechat( Base ) :
    __table__ = Table( 'wechat' , metadata , autoload = True )
    user = relationship( 'user' , back_populates = 'wechats' )
    def __repr__( self ) :
        return 'wechat-id : %d' % self.id
class user( Base ) :
    __table__ = Table( 'user' , metadata , autoload = True )
    student = relationship( 'student' , uselist = False , back_populates = 'user' )
    claxx_teacher = relationship( 'claxx_teacher' , uselist = False , back_populates = 'user' )
    wechats = relationship( 'wechat' , back_populates = 'user' )
    def __repr__( self ) :
        return 'user-id : %d' % self.id
class student( Base ) :
    __table__ = Table( 'student' , metadata , autoload = True )
    claxx = relationship( 'claxx' , back_populates = 'students' )
    claxx_teacher = relationship( 'claxx_teacher' , back_populates = 'students' )
    dormitory = relationship( 'dormitory' , back_populates = 'students' )
    building = relationship( 'building' , back_populates = 'students' )
    user = relationship( 'user' , back_populates = 'student' )
    def __repr__( self ) :
        return 'student-id : %d' % self.id
class claxx_teacher( Base ) :
    __table__ = Table( 'claxx_teacher' , metadata , autoload = True )
    dormitories = relationship( '_claxx_teacher_to_dormitory' , back_populates = 'claxx_teacher' )
    buildings = relationship( '_claxx_teacher_to_building' , back_populates = 'claxx_teacher' )
    students = relationship( 'student' , back_populates = 'claxx_teacher' )
    claxxes = relationship( 'claxx' , back_populates = 'claxx_teacher' )
    user = relationship( 'user' , back_populates = 'claxx_teacher' )
    def __repr__( self ) :
        return 'claxx_teacher-id : %d' % self.id
class claxx( Base ) :
    __table__ = Table( 'claxx' , metadata , autoload = True )
    dormitories = relationship( '_claxx_to_dormitory' , back_populates = 'claxx' )
    buildings = relationship( '_claxx_to_building' , back_populates = 'claxx' )
    students = relationship( 'student' , back_populates = 'claxx' )
    claxx_teacher = relationship( 'claxx_teacher' , back_populates = 'claxxes' )
    def __repr__( self ) :
        return 'claxx-id : %d' % self.id
class dormitory( Base ) :
    __table__ = Table( 'dormitory' , metadata , autoload = True )
    claxxes = relationship( '_claxx_to_dormitory' , back_populates = 'dormitory' )
    claxx_teachers = relationship( '_claxx_teacher_to_dormitory' , back_populates = 'dormitory' )
    students = relationship( 'student' , back_populates = 'dormitory' )
    building = relationship( 'building' , back_populates = 'dormitories' )
    def __repr__( self ) :
        return 'dormitory-id : %d' % self.id
class building( Base ) :
    __table__ = Table( 'building' , metadata , autoload = True )
    claxxes = relationship( '_claxx_to_building' , back_populates = 'building' )
    claxx_teachers = relationship( '_claxx_teacher_to_building' , back_populates = 'building' )
    students = relationship( 'student' , back_populates = 'building' )
    dormitories = relationship( 'dormitory' , back_populates = 'building' )
    def __repr__( self ) :
        return 'building-id : %d' % self.id
    
def test( ) :
    session = sessionmaker( engine )( )
    s = session.query( student ).filter( student.id == 1 ).first( )
    ct = session.query( claxx_teacher ).join( student ).filter( student.id == 1 ).first( )
    d = session.query( dormitory ).join( student ).filter( student.id == 1 ).first( )
    c = session.query( claxx ).join( student ).filter( student.id == 1 ).first( )
    b = session.query( building ).join( student ).filter( student.id == 1 ).first( )
    print( s.claxx_teacher )
    print( s.dormitory )
    print( s.claxx )
    print( s.building )
def db_check_openid( openid ) :
    w = session.query( wechat ).filter( wechat.openid == openid ).first( )
    return not( w == None )
def db_check_user_and_add_openid( username , password , openid ) :
    rc = ''
    u = session.query( user ).filter( user.username == username ).first( )
    if u == None :
        rc = 'unknow_user'
    else :
        if u.password == password :
            rc = 'success'
            w = wechat( )
            if( u.student == None ) :
                w.user_type = 'claxx_teacher'
            else :
                u.user_type = 'student'
            w.user = u
            w.openid = openid
            session.add( u )
            session.flush( )
            session.commit( )
        else :
            rc = 'password_error'
    return rc
def db_get_wechat_info( openid ) :
    rc = {
        'user_type' : ''
    }
    w = session.query( wechat ).filter( wechat.openid == openid ).first( )
    if not w == None :
        rc['user_type'] = w.user_type
    return rc
def db_get_teacher_info( openid ) :
    rc = {
        'user_type' : ''
    }
    w = session.query( wechat ).filter( wechat.openid == openid ).first( )
    if not w == None :
        rc['teacher_name'] = w.user.claxx_teacher.name
    return rc
def db_get_students_info_by_teacher_openid( openid ) :
    rc = {
        'user_type' : ''
    }
    w = session.query( wechat ).filter( wechat.openid == openid ).first( )
    if not w == None :
        rc['students'] = [ student.name for student in w.user.claxx_teacher.students ]
    return rc

if __name__ == '__main__' :
    test( )
