changes_table = """
<table style="border-collapse:collapse;border-spacing:0;table-layout: fixed; width: 782px" class="tg">
<colgroup>
    <col style="width: 81px">
    <col style="width: 701px">
</colgroup>
<thead>
    <tr>
        <th
            style="border-color:inherit;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">
            Product:</th>
        <th
            style="border-color:inherit;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">
            {product}</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td
            style="border-color:inherit;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">
            Key:</td>
        <td
            style="border-color:inherit;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">
            {key}</td>
    </tr>
    <tr>
        <td
            style="background-color:#ffccc9;border-color:inherit;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">
            Was:</td>
        <td
            style="background-color:#ffccc9;border-color:inherit;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">
            {old_value}</td>
    </tr>
    <tr>
        <td
            style="background-color:#ffcc67;border-color:inherit;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:bold;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">
            Now:</td>
        <td
            style="background-color:#ffcc67;border-color:inherit;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;text-align:left;vertical-align:top;word-break:normal">
            {new_value}</td>
    </tr>
</tbody>
</table>
"""

warning_body = """
<html>
<head></head>
<body>
    <h1>VFX Python 3 Readiness</h1>
    <p style='font-weight: 700; background-color:black; color:rgb(255, 208, 0)'>
        Warning:
    </p>
    <p style='margin-left: 40px'>{0}</p>
</body>
</html>
"""
