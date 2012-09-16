<html>
<head>
	<link rel="stylesheet" type="text/css" href="/static/style.css" />
</head>
<body>

<div id="main">
%prev_date = "0000-00-00"
%for post in posts:
%   if post[0] == prev_date:
<br />
<center>~</center><br />
{{post[1]}}
%   else:
</div>
<div class="day_entry">
{{post[0]}}<br /><br />
{{post[1]}}
%   prev_date = post[0]
%end
%end


</div>
</body>
</html>