// Implement search funcionality for traffic lights page.


// Find company and show error message if not found.

function findCompany(name, companies) {
  for (let i = 0; i < companies.length; i++) {
    if (name == companies[i].innerHTML) {
      window.location.hash = '#' + name;
      $("#" + name).focus();
      $(".not-found").remove();
      return; // Terminate function
    }
  }
  if ($(".not-found").length == 0) {
    $(".search-bar").append("<div class='not-found'>Company not found</div>");
  }
}


// Make list of all companies loaded from databse.

function addCompanies() {
  var companies = $(".company-name");
  var names = []
  for (let i = 0; i < companies.length; i++) {
    names.push(companies[i].innerHTML);
  }
  return names;
}


// Execute when document is ready.

$(document).ready(function() {
  var companies = $(".company-name");
  var names = addCompanies();

  // Add auto completion.

  $(".search-bar input").autocomplete({
    source: names,
    appendTo: ".search-bar > ul",
    open: function () {
      if($(".not-found").length == 1) {
        $(".not-found").remove();
      }
    }
  });

  // Search for company when Enter is pressed.

  $(".search-bar input").keyup(function (event) {
    if (event.key == "Enter") {
      findCompany($(".search-bar input").val(), companies);
    }
  });
});
