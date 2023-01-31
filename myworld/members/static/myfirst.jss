function myFunction() {
  alert("Hello from a static file. Does this display?");
  console.log("Does this display?");
 /* var all = document.getElementsByTagName("*");
  for (let i=0, max = all.length; i<max; i++)
  {
    console.log(all[i]);
  }*/
//document.querySelector('#chat-log').value = "";
}

// alert("work now!");

function getRandomIntInclusive(min, max) {
    min = Math.ceil(min)
    max = Math.max(max)
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function pointify(msg){
	const zip = (a, b) => a.map((k, i) => [k, b[i]]);
      msg = zip(msg[0],msg[1]);
      var str = "";
      for (let i = 0; i<msg.length;i++)
      {
         str += "(" + msg[i][0] + ", " + msg[i][1] + "), ";
      }

	str = str.slice(0,-2);

	return str;

}

console.log("hi!");

var chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/members/'
        );
//}

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
    };

chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
		//alert(data.message.split());
            var my_plot = {
            x: data.message[0], 
            y: data.message[1], 
            type: 'scatter',
           // opacity: 0.8,
        };
  		Plotly.newPlot('sine-graph', [my_plot]);
            var curr = document.querySelector('#chat-log').value;
		var count = document.querySelector('#chat-log').value.split("\n").length-1;
            //alert(count);
            
            if (count==15)
            {
                 document.querySelector('#chat-log').value = (pointify(data.message) + '\n');
            }
            else
            {
                document.querySelector('#chat-log').value += (pointify(data.message) + '\n');
            }
            //alert(count);
            
        };

var myfunc = setInterval(function(){
    x = [];
    y = [];
   
    for (let i = 0; i < 5; i++)
    {
        temp1 = getRandomIntInclusive(1,10);
        temp2 = getRandomIntInclusive(1,10);
        x.push(temp1);
        y.push(temp2);
    }

    chatSocket.send(JSON.stringify({
                'text_data': [x,y]
            }));
}, 500);

function Stop()
{
    chatSocket.close();
}

function Clear()
{
    document.querySelector('#chat-log').value = "";
}

function Start()
{
    Stop();
    chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/members/'
        );

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        };

    chatSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                //alert(data.message[0]);
                var my_plot = {
                x: data.message[0],
                y: data.message[1],
                type: 'scatter',
               // opacity: 0.8,
            };
              Plotly.newPlot('sine-graph', [my_plot]);
                var curr = document.querySelector('#chat-log').value;
            var count = document.querySelector('#chat-log').value.split("\n").length-1;
                //alert(count);
                
                if (count==15)
                {
                     document.querySelector('#chat-log').value = (pointify(data.message) + '\n');
                }
                else
                {
                    document.querySelector('#chat-log').value += (pointify(data.message) + '\n');
                }
                //alert(count);
                
            };

    var myfunc = setInterval(function(){
        x = [];
        y = [];
       
        for (let i = 0; i < 5; i++)
        {
            temp1 = getRandomIntInclusive(1,10);
            temp2 = getRandomIntInclusive(1,10);
            x.push(temp1);
            y.push(temp2);
        }

        chatSocket.send(JSON.stringify({
                    'text_data': [x,y]
                }));
    }, 500);
}

