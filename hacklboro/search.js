// Implement search funcionality for traffic lights page.

$(document).ready(function() {
  var names = [];
  var companies = $(".company-name");
  for (let i = 0; i < companies.length; i++) {
    names.push(companies[i].innerHTML);
  }

  $(".search-bar > input").autocomplete({
    source: names,
    appendTo: ".search-bar"
  });
  $(".search-bar > input").keyup(function (event) {
    if (event.key == "Enter") {
      focusCard($(".search-bar > input").val());
    }
  });

  function focusCard(name) {
    for (let i = 0; i < companies.length; i++) {
      if (name == companies[i].innerHTML) {
        window.location.hash = '#' + name;
        $("#" + name).focus();
        return; // Terminate function
      }
    }
    alert("Company \"" + name + "\" has not been found");
    $(".search-bar").append("<p class='not-found'>Company not found</p>");
  }
});
