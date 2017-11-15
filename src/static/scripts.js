function number_format(number, decimals, decPoint, thousandsSep) {
  // Source: http://locutus.io/php/strings/number_format/

  number = (number + '').replace(/[^0-9+\-Ee.]/g, '')
  var n = !isFinite(+number) ? 0 : +number
  var prec = !isFinite(+decimals) ? 0 : Math.abs(decimals)
  var sep = (typeof thousandsSep === 'undefined') ? ',' : thousandsSep
  var dec = (typeof decPoint === 'undefined') ? '.' : decPoint
  var s = ''

  var toFixedFix = function (n, prec) {
    var k = Math.pow(10, prec)
    return '' + (Math.round(n * k) / k)
      .toFixed(prec)
  }

  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.')
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep)
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || ''
    s[1] += new Array(prec - s[1].length + 1).join('0')
  }

  return s.join(dec)
}

$.getJSON("status.json", function(data) {
  // Format & fill the amount of online users
  $("#steam_users").text(number_format(data.steam_users, 0, "", " "));

  // Fill the steam services
  $.each(data.steam_services, function(index, value) {
    if (value == 200)
      value = "online"
    else if (!isNaN(value))
      value = "HTTP Status Code " + value

    $("#" + index).text(value);
  });

  // Fill the CS:GO services
  $.each(data.csgo_services, function(index, value) {
    $("#" + index).text(value);
  });

  // Fill the CS:GO servers
  $.each(data.csgo_servers, function(index, value) {
    index = index.toLowerCase().replace(/\s+/g, "_");
    $("#" + index).text(value);
  });
})
.done(function() {
  // Keywords to color the statuses differently
  var good_status = ["idle",  "low",  "normal",  "online"]
  var okay_status = ["delayed", "medium"]
  var bad_status = ["high", "offline"]

  $(".status").each(function() {
    var text = $(this).text();
    if (good_status.includes(text))
      $(this).css("color", "#6C9541");
    else if (okay_status.includes(text))
      $(this).css("color", "#53A4C4");
    else if (bad_status.includes(text))
      $(this).css("color", "#F44336");
  });
})
.fail(function(jqXHR) {
    var errmsg = $($.parseHTML(jqXHR.responseText)).closest("p").text();
    errmsg = "HTTP Status Code " + jqXHR.status + ": " + errmsg;

    $("#servermsg").addClass("alert-danger");
    $("#servermsg").append(errmsg);
    $("#servermsg").removeAttr("style");
});
