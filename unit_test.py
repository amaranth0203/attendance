
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine , MetaData , Table , func
from sqlalchemy.orm import sessionmaker , mapper , relationship
from sqlalchemy.ext.declarative import declarative_base


import unittest

engine = create_engine( 'mysql+pymysql://attendance:echo@localhost/attendance?charset=utf8' , echo=False , encoding='utf-8' )
metadata = MetaData( engine )
Base = declarative_base( )
Base.metadata = metadata

class Class( Base ) :
    __table__ = Table( 'class' , metadata , autoload = True )
    class_teacher = relationship( 'Class_teacher' , backref = 'class' )
    def __repr__( self ) :
        return 'Class-id : %d' % self.id ;
class Class_teacher( Base ) :
    __table__ = Table( 'class_teacher' , metadata , autoload = True )
    def __repr__( self ) :
        return 'Class_teacher-id : %d' % self.id ;
class Student( object ) :
    __table__ = Table( 'student' , metadata , autoload = True )
    def __repr__( self ) :
        return 'Student-id : %d' % self.id ;
class Dormitory( object ) :
    __table__ = Table( 'dormitory' , metadata , autoload = True )
    def __repr__( self ) :
        return 'Dormitory-id : %d' % self.id ;
class _class_to_dormitory :
    __table__ = Table( '_class_to_dormitory' , metadata , autoload = True )
    pass

class TestSQLAlchemy( unittest.TestCase ) :

    def setUp( self ) :
        self.engine = create_engine( 'mysql+pymysql://attendance:echo@localhost/attendance?charset=utf8' , echo=False , encoding='utf-8' )
        print( '\n[+] setUp...' )

    def tearDown( self ) :
        print( '[+] tearDown...' )

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
#        metadata = MetaData( self.engine )
#        class_t = Table( 'class' , metadata , autoload = True )
#        student_t = Table( 'student' , metadata , autoload = True )
#        dormitory_t = Table( 'dormitory' , metadata , autoload = True )
#        class_teacher_t = Table( 'class_teacher' , metadata , autoload = True )
#        _class_to_dormitory_t = Table( '_class_to_dormitory' , metadata , autoload = True )
        Session = sessionmaker( self.engine )
        session = Session( )
#        mapper( Class , class_t , non_primary = True )
#        mapper( Student , student_t )
#        mapper( Dormitory , dormitory_t )
#        mapper( Class_teacher , class_teacher_t , non_primary = True )
#        mapper( _class_to_dormitory , _class_to_dormitory_t )
        c = session.query( Class ).first( )
        print( '----------------------------------------' )
        print( c.class_teacher )
        print( '----------------------------------------' )
#        t = session.query( Student ).first( )
#        print( session.query( Student ).join( Class , isouter = True ).filter( Class.id == 2 ).all( ) )
#        dormitory_obj = session.query( Dormitory ).filter( Dormitory.id == 3 ).first( )
#        class_to_dormitory = session.query( _class_to_dormitory.class_id ).filter( _class_to_dormitory.dormitory_id == dormitory_obj.id ).all( )
#        r = zip( *class_to_dormitory )
#        print( '----' )
#        print( session.query( Class ).filter( Class.id.in_(list(list(r)[0])) ).all( ) )
#        print( '****' )

    

if __name__ == '__main__' :
    unittest.main( )
            
        
