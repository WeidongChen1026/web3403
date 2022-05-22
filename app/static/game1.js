      function random(min, max) { return Math.floor(Math.random() * (max - min)) + min; }

      $(function(){
        $("#num_times").text(10)
        $("#model_val").text(10)

        var temp_val = random(1,100);
        $("#rd_val").text(temp_val);
      })

      function change_model(num_vals){
        $("#num_times").text(num_vals);
        $("#model_val").text(num_vals);
        var ee = document.getElementById("num_val");
        ee.value = "";
      }

      function val_check(){
        var ee = document.getElementById("num_val").value;
        var eee = $("#num_times").html();
        var e = $("#rd_val").html();

        if(eee=="0"){
          $("#tips").text("You have no chance.");
            pass();
        }else if(ee==""){
          $("#tips").text("Please enter the value you want to guess first!");
        }else{
          $("#num_times").html($("#num_times").html()-1)
          if(ee>e){
            $("#tips").text("Your guess is a little higher.");
          }else if(ee<e){
            $("#tips").text("Your guess is a little low");
          }else{
            $("#tips").text("Congratulations!!!");
            pass();

            var tmp_res = "Guess number <br> The number I guessed is " + e + ", and there is still " + $("#num_times").html() + " chances remain."
            document.getElementById("result").innerHTML= tmp_res;
            document.getElementById("share").style.display = "inline";
            document.getElementById('share').addEventListener('click', function() {
              var isCopyed = copyDiv();
              tips(isCopyed);
		}, false);
            re_init()

          }
        }
      }

      function re_init(){
        var model_val = $("#model_val").text()
        $("#num_times").text(model_val)

        var temp_val = random(1,100);
        $("#rd_val").text(temp_val);

        $("#num_val").val('')
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
        var user = document.getElementById('hahah').innerHTML;
        if(document.getElementById('tips').innerHTML=="Congratulations!!!"){
           success = true;
         };
        var chance_remain = document.getElementById('num_times').innerText;
        var data = {
                "username":user,
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