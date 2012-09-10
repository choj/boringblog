<p>register your boring blog</p>

%if error == "bad_email":
    <p><b>Invalid email.</b></p>
%elif error == "pw_mismatch":
    <p><b>Passwords don't match.</b></p>
%elif error == "email_exists":
    <p><b>Email already registered.</b></p>
%end

<form action="/register" method="GET">
    <input type="text" size="64" maxlength="64" name="email" value="email"><br />
    <input type="password" size="64" maxlength="64" name="password" value="password"><br />
    <input type="password" size="64" maxlength="64" name="confirm" value="password"><br />
    <input type="submit" name="register" value="register">
</form>