fetch("https://www.kiwi.com")
  .then(response => response.text())
  .then(data => {
    console.log(data.price);
  })    