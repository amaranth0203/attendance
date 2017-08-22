
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine , MetaData , Table , func
from sqlalchemy.orm import sessionmaker , mapper , relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import *
from sqlalchemy.orm import *


import unittest

engine = create_engine( 'mysql+pymysql://attendance:echo@localhost/attendance?charset=utf8' , echo=False , encoding='utf-8' )
metadata = MetaData( engine )
Base = declarative_base( )
Base.metadata = metadata

class _claxx_teacher_to_building( Base ) :
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
class user( Base ) :
    __table__ = Table( 'user' , metadata , autoload = True )
    student = relationship( 'student' , uselist = False , back_populates = 'user' )
    claxx_teacher = relationship( 'claxx_teacher' , uselist = False , back_populates = 'user' )
    wechats = relationship( 'wechat' , back_populates = 'user' )
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

class TestSQLAlchemy( unittest.TestCase ) :

    def setUp( self ) :
        pass
        self.engine = create_engine( 'mysql+pymysql://attendance:echo@localhost/attendance?charset=utf8' , echo=False , encoding='utf-8' )
#        print( '\n[+] setUp...' )

    def tearDown( self ) :
        pass
#        print( '[+] tearDown...' )

    def ttest_init( self ) :
        self.assertEqual( 'a' , 'a' )
        print( '[+] this is test_init' )

    def ttest_equal( self ) :
        self.assertEqual( 1 , 1 )
        print( '[+] this is test_equal' )
        
    def ttest_true( self ) :
        self.assertTrue( 'True' )
        print( '[+] this is test_true' )

    def ttest_reflection( self ) :
        print( '[+] test_reflection' )
        metadata = MetaData( self.engine )
        print( 'class' in metadata )
        print( 'class_teacher' in metadata )
        class_t = Table( 'class' , metadata , autoload = True )
        print( 'class' in metadata )
        print( 'class_teacher' in metadata ) # fk key
        print( [ c.name for c in class_t.columns ] )

    def ttest_query( self ) :
        print( '[+] test_query' )
        metadata = MetaData( self.engine )
        class_t = Table( 'class' , metadata , autoload = True )
        Session = sessionmaker( self.engine )
        session = Session( )
        print( '****************************************' )
        [ print( c ) for c in session.query( class_t ).all( ) ]
        print( '****************************************' )
        [ print( c ) for c in session.query( class_t ).filter_by( id = 0 ).all( ) ]
        print( '****************************************' )
        [ print( c ) for c in session.query( class_t ).filter( class_t.name == 'class' ).all( ) ]
        print( '****************************************' )
        [ print( c ) for c in session.query( class_t ).filter_by( id = 0 ).all( ) ]
        print( '****************************************' )

    def ttest_add( self ) :
        print( '[+] test_add' )
        metadata = MetaData( self.engine )
        class_t = Table( 'class' , metadata , autoload = True )
        Session = sessionmaker( self.engine )
        session = Session( )
        mapper( Class , class_t )
        c = Class( )
        c.name = "汽修1班"
        session.add( c )
        session.flush( )
        session.commit( )
        
    def ttest_update( self ) :
        print( '[+] test_update' )
        metadata = MetaData( self.engine )
        class_t = Table( 'class' , metadata , autoload = True )
        Session = sessionmaker( self.engine )
        session = Session( )
        mapper( Class , class_t )
        session.query( Class ).filter( Class.id > 1 ).update( { 'name' :  "2" } )
        session.query( Class ).filter( Class.id > 0 ).update( { Class.name : Class.name + "1" } , synchronize_session = False )
        session.commit( )

    def ttest_delete( self ) :
        print( '[+] test_delete' )
        metadata = MetaData( self.engine )
        class_t = Table( 'class' , metadata , autoload = True )
        Session = sessionmaker( self.engine )
        session = Session( )
        mapper( Class , class_t )
        session.query( Class ).filter( Class.id > 2 ).delete( )
        session.commit( )

    def test_add2( self ) :
        print( '[+] test_add2' )
        Session = sessionmaker( self.engine )
        session = Session( )
        c = session.query( claxx ).first( )
        s = session.query( student ).first( )
        d = session.query( dormitory ).filter( dormitory.id == 3 ).first( )
        ct = session.query( claxx_teacher ).filter( claxx_teacher.id == 1 ).first( )
#        assoc = _class_to_dormitory( )
#        assoc.classs = c
#        d = Dormitory( )
#        d.classes.append( assoc )
#        session.add( d )
#        session.flush( )
#        session.commit( )
        print( '----------------------------------------' )
        print( c )
        print( c.students )
        print( s.claxx == c )
        print( s.claxx_teacher )
        print( [ assoc.dormitory for assoc in c.dormitories ] )
        print( '-----------------*-----------------------' )
        print( [ assoc.claxx_teacher for assoc in d.claxx_teachers ] )
        print( [ assoc.dormitory for assoc in ct.dormitories ] )
        print( '----------------------------------------' )

#        t = session.query( Student ).first( )
#        print( session.query( Student ).join( Class , isouter = True ).filter( Class.id == 2 ).all( ) )
#        dormitory_obj = session.query( Dormitory ).filter( Dormitory.id == 3 ).first( )
#        class_to_dormitory = session.query( _class_to_dormitory.class_id ).filter( _class_to_dormitory.dormitory_id == dormitory_obj.id ).all( )
#        r = zip( *class_to_dormitory )
#        print( '----' )
#        print( session.query( Class ).filter( Class.id.in_(list(list(r)[0])) ).all( ) )
#        print( '****' )

    def test_student( self ) :
        print( '[+] test_student' )
        session = sessionmaker( self.engine )( )
        s = session.query( student ).filter( student.id == 1 ).first( )
        ct = session.query( claxx_teacher ).join( student ).filter( student.id == 1 ).first( )
        d = session.query( dormitory ).join( student ).filter( student.id == 1 ).first( )
        c = session.query( claxx ).join( student ).filter( student.id == 1 ).first( )
        b = session.query( building ).join( student ).filter( student.id == 1 ).first( )
        self.assertEqual( s.claxx_teacher , ct )
        self.assertEqual( s.dormitory , d )
        self.assertEqual( s.claxx , c )
        self.assertEqual( s.building , b )
        s1 = student( )
        s1.name = 'tester'
        s1.student_number = 'tester_number'
        u = user( )
        u.username = s1.name
        s1.user = u
        session.add(s1)
        session.flush( )
        session.commit( )
#        u = session.query( user ).filter( user.student.name == 'tester' ).all( )
#        print( u.id )

    def test_claxx_teacher( self ) :
        print( '[+] test_claxx_teacher' )
        session = sessionmaker( self.engine )( )
        t = session.query( claxx_teacher ).filter( student.id == 1 ).first( )
#        self.assertEqual( t.
        
    
if __name__ == '__main__' :
    unittest.main( )
            
        
