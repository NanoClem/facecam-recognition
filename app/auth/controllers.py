from flask import flash, redirect
import bcrypt



def hash_password(password: str, salt: bytes=bcrypt.gensalt(), key_bytes:int=32, rounds: int=12) -> str:
    """[summary]
    
    Parameters
    -----
        password (str) -- [description]
        salt (str) -- [description]
        key_bytes (int) -- [description] (default: 32)
        rounds (int) -- [description] (default: 12)
    
    Returns
    -----
        str -- [description]
    """
    hash = bcrypt.kdf(
        password=str.encode(password),
        salt=salt,
        desired_key_bytes=key_bytes,
        rounds=rounds
    )
    return hash



def check_password(hash_psswd: str) -> bool:
    """Check for matching hash in database of the given password
    
    Parameters
    -----
        hash_psswd (str) -- hash version of a user's password input
    
    Returns
    -----
        bool -- hashed password matched in database or not
    """
    ## TODO: request api to check user password
    db_psswd = ""
    return True #bcrypt.checkpw(db_psswd, hash_psswd)



def check_credentials(username: str, hash_psswd: str) -> bool:
    """Check user credentials in database
    
    Returns
    -----
        bool -- [description]
    """             
    return check_password(hash_psswd)    ##TODO: check email in db



def login_user(form) -> bool:
    """Log a user by checking form validation and user credentials
    
    Parameters
    -----
        form (flask_wtf.FlaskForm) -- form class with user credentials

    Returns
    -----
        bool -- User successfuly loged in or not
    """
    if form.validate_on_submit():
        username    = form.username.data
        password    = hash_password(form.password.data)
        remember_me = form.remember_me.data
        # temp log message
        flash('Login requested for user {}, remember_me={}'.format(username, remember_me))
        return check_credentials(username, password)
    
    return False