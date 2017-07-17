
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine , MetaData , Table
from sqlalchemy.orm import sessionmaker , mapper


import unittest

class Class( object ) :
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

    

if __name__ == '__main__' :
    unittest.main( )
            
        
