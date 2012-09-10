<p>login to your boring blog</p>

%if error == "bad_login":
<p><b>Invalid email/password</b></p>
%end

<form action="/login" method="GET">
    <input type="text" size="64" maxlength="64" name="email" value="email"><br />
    <input type="password" size="64" maxlength="64" name="password" value="password"><br />
    <input type="submit" name="login" value="login">
</form>