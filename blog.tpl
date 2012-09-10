
%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)

<table border="1">
%for row in rows:
  <tr>
    <td>{{row[2][0:10]}}<br />{{row[4]}}</td>
  </tr>
%end
</table>