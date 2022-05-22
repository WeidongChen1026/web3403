      function random(min, max) { return Math.floor(Math.random() * (max - min)) + min; }

      window.onload = function(){
        $("#num_times").text(10)
        $("#score_val").text(0)

        var temp_val = random(1,100);
        $("#rd_val").text(temp_val);

        var table = document.createElement("table");
        table.setAttribute("border","1");
        table.setAttribute("width","15%");

        var cap = table.createCaption();
        cap.innerHTML= "Ranking List";

        for(var i =1;i<6;i++){
          var tr = document.createElement("tr");
          var td_na = document.createElement("td")
          td_na.innerHTML= "Name";
          var td_nu = document.createElement("td")
          td_nu.innerHTML= 0;
          tr.appendChild(td_na);
          tr.appendChild(td_nu);

          table.appendChild(tr);
        }
        document.getElementById("tb_cr").appendChild(table);

      };

      function change_model(num_vals){
        $("#num_times").text(num_vals);
        var ee = document.getElementById("num_val");
        ee.value = "";
      }

      function val_check(){
        var ee = document.getElementById("num_val").value;
        var eee = $("#num_times").html();
        var e = $("#rd_val").html();

        if(eee=="0"){
          $("#tips").text("You have no chance.");
        }else if(ee==""){
          $("#tips").text("Please enter the value you want to guess first!");
        }else{
          $("#num_times").html($("#num_times").html()-1)
          if(ee>e){
            $("#tips").text("Your guess is a little higher.");
          }else if(ee<e){
            $("#tips").text("Your guess is a little low");
          }else{
            $("score_val").html($("#score_val").html()+1)
            $("#tips").text("Congratulations!!!");
            // pass();
            document.getElementById("result").innerHTML="Guess number <br> The number I guessed is(加入猜了的数字)," +
                " and there is still (还剩几次) chances remain";
            document.getElementById("share").style.display = "inline";
            document.getElementById('share').addEventListener('click', function() {
              var isCopyed = copyDiv();
              tips(isCopyed);
		}, false);
            window.location.reload();
            reload_i();
            window.location.reload();
          }
        }
      }

      function reload_i(){
        window.location.reload();
      }

      function tips(status) {
		  if (status) {
		    alert('Copy success');
		  } else {
		    alert('Copy failed, please select the content and copy manually.');
		  }
		}

      function pass(){//TODO:pass the data from front-end to back-end
        var success = false;
        if(document.getElementById('tips').innerHTML=="Congratulations!!!"){
           success = true;
         };
        var chance_remain = document.getElementById('num_times').innerText;
        var data = {
              "is_success": success,
              "chance_remain": chance_remain
          };
          $.ajax({
              type: 'GET',
              url: "http://localhost:5000/record",
              data: data,
              dataType: 'json',
              success: function(data) {
              },
              error: function(xhr, type) {
              }
          });}

      function copyDiv() {//share
		  var range = document.createRange();
		  range.selectNode(document.getElementById("result"));
		  var selection = window.getSelection();
		  if (selection.rangeCount > 0) selection.removeAllRanges();
		  selection.addRange(range);
		  return document.execCommand('copy');
		}

