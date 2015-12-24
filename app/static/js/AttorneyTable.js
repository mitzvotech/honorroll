
var AttorneyTable = function () {
  $("#honorroll").toggle();
  $.getJSON('/api/attorneys', function (data) {

    var attorneys = data.filter(function (d) {
      if (d["records"].length > 0) {
        return d["records"][d["records"].length - 1].year == '2015';
      }
    }).map(function (d) {
      d.honors = d["records"][d["records"].length - 1].honor_choice;
      return {
        'first_name': d.first_name,
        'last_name': d.last_name,
        'organization_name': d.organization_name,
        'year': '2015',
        'honors': d.honors
      }
    });


    $('#honorroll').DataTable({
      "data": attorneys,
      "columns": [
        { "title": "First Name", "data": "first_name" },
        { "title": "Last Name", "data": "last_name" },
        { "title": "Organization Name", "data": "organization_name" },
        { "title": "Year", "data": "year" },
        { "title": "Honors", "data": "honors"}
      ],
      'order':[[2,'asc'],[0,'asc']],
      "fnDrawCallback": cleanDOM()
    });
  })
}

function cleanDOM () {
  $('#honorroll_wrapper').toggle();
  $('#honorroll').toggle();
  $('#loading').html('')
}
