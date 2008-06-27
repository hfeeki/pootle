# login.py
# A set of jToollkit style login checkers 

# Author: Dan Schafer <dschafer@mozilla.com>
# Date: 16 Jun 2008


# The Mozilla LDAP package. 
import mozldap

from jToolkit import web

class LDAPLoginChecker(web.session.LoginChecker):
  """A login checker that uses users.prefs files for preferences, but
  LDAP for user authentication.  This extends LoginChecker to get its
  implementation of preferences; since LDAP does not support getting
  the MD5 of the password, that method now throws an exception.

  """

  def userexists(self, username=None):
    """Checks whether user username exists as a valid LDAP username; note
    that this is not checking if it is a valid distinguished name!  What
    username means here is left to the particular LDAP implementation.  Under
    the standard implementation of mozldap, this will use the mozldap
    library to see if the given username is a valid e-mail address in the
    directory, since e-mails are the usernames for Mozilla LDAP.
    
    """
    
    if username is None:
      username = self.session.username
    c = mozldap.MozillaLdap()
    return c.hasAccount(username)

  def iscorrectpass(self, password, username=None):
    """Checks whether 'password' is the correct password for user 'username'
    Using the standard mozldap implementation, this will find the
    dinstinguished name for the user with e-mail address 'username', then
    try and bind with that distinguished name and 'password'  If all of this
    succeeds, then this is a valid username/password combination; otherwise,
    it is not.
    
    """
    
    if username is None:
      username = self.session.username
    c = mozldap.MozillaLdap()
    return c.isCorrectCredentials(username, password)

  def getmd5password(self, username=None):
    """Not supported by Mozilla's LDAP; it is possible that in someone else's
    LDAP system, one can get the MD5.
    
    """

    raise NotImplementedError


class HashLoginChecker(web.session.LoginChecker):
  """A login checker duplicating the capabilities of the default LoginChecker,
  but supporting the iscorrectpass method.
  
  """

  def iscorrectpass(self, password, username=None):
    import md5
    if username is None:
      username = self.session.username
    return md5.md5(password).hexdigest() == self.getmd5password(username) 

class ProgressiveLoginChecker(web.session.LoginChecker):
  """A login checker that looks at a preference set in the user's entry
  in users.prefs to determine what LoginChecker to use.  It has the same
  interface as LDAPLoginChecker and HashLoginChecker.

  """

  def __init__(self, session, instance, logindict):
    web.session.LoginChecker.__init__(self, session, instance)
    self.logincheckers = logindict

  def getAcctNode(self, username):
    import re
    dotsafeusername = re.sub("\.","D0T",username)
    try:
      return self.users.__getattr__(dotsafeusername)
    except AttributeError:
      raise self.NoSuchUser("Given username (%s) has no account" % username)

  def getChecker(self, username):
    n = self.getAcctNode(username)
    try:
      return self.logincheckers[n.logintype]
    except AttributeError:
      raise AttributeError("Given username (%s) has no login type lister" % username)
    except KeyError:
      raise self.NoSuchLoginChecker("Given username (%s) LoginChecker does not exist" % username)

  def userexists(self, username=None, create=False):
    """This function checks to see if the user exists; namely, does the user
    have an entry in the preferences file.  If it does not, this will go
    through the list of LoginCheckers, seeing if this user exists in one
    of them.  If the user does and create is on, this function will make
    them a preferences entry and return True.

    """ 

    if username is None:
      username = self.session.username
    
    try:
      acct = self.getAcctNode(username) 
    except self.NoSuchUser:
      return False
    else:
      return True

  def iscorrectpass(self, password, username=None):
    if username is None:
      username = self.session.username
    
    try:
      checker = self.getChecker(username)
    except self.NoSuchUser:
      return False
    return checker.iscorrectpass(password, username)

  def getmd5password(self, username=None):
    if username is None:
      username = self.session.username
    
    checker = self.getChecker(username)
    return checker.getmd5password(username)

  class NoSuchUser(Exception):
    pass
  
  class NoSuchLoginChecker(Exception):
    pass
