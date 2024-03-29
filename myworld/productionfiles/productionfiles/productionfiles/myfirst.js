//⌄⌄⌄ Open SideBar
function openNav()
{
    document.getElementById("mySidenav").style.width = "250px";
}

//⌄⌄⌄ Close SideBar
function closeNav()
{
    document.getElementById("mySidenav").style.width = "0";
}

//⌄⌄⌄ fired when you drag something over the document
document.body.addEventListener('dragover', function(event)
{
    event.preventDefault(); //prevents default behaviour
    return false; //prevents the default action
});

//⌄⌄⌄ function used for dragstart EventListener
function startDrag(event)
{
//    https://stackoverflow.com/a/6239882/18255427
    var style = window.getComputedStyle(event.target, null);
    window.offset = (parseInt(style.getPropertyValue("left"),10) - event.clientX) + ',' + (parseInt(style.getPropertyValue("top"),10) - event.clientY);
    if (window.offset.split(",").some(element => !parseInt(element)))
    {
        window.offset = "0,0";
    }
}

//⌄⌄⌄ function used for dragend EventListener
function endDrag(event)
{
//    https://stackoverflow.com/a/6239882/18255427
    var offset = window.offset.split(',');
    let left = (parseInt(offset[0],10) ? (event.clientX + parseInt(offset[0],10)) : event.clientX);
    let top = (parseInt(offset[1],10) ? (event.clientY + parseInt(offset[1],10)) : event.clientY);
    
    let rect = event.target.getBoundingClientRect();
    event.target.style.left = left ? left + 'px' : rect.left + "px";
    event.target.style.top = top ? top + 'px' : rect.top + "px";
    
    if (possibleHTMLelements[event.target.getAttribute("id")] !== undefined)
    {
        possibleHTMLelements[event.target.getAttribute("id")]["coordinates"] = [left, top];
    }
    event.preventDefault();
    return false;
};

//⌄⌄⌄ fired when you click "Add Basic Animation"
function basicAnimation()
{
    var border = document.createElement('mydiv'); //create a mydiv element
    border.id = "border_id"; //assign an id
    border.className = 'outer_square'; //the animation takes place in the border element
    border.draggable= "true"; //make draggable
    border.position = "relative"; //https://www.w3schools.com/css/css_positioning.asp
    
    //⌄⌄⌄ behaviour when user starts dragging this element
    border.addEventListener('dragstart', startDrag, true);
    //⌄⌄⌄ behaviour when user stops dragging this element
    border.addEventListener('dragend', endDrag, true);
    
    var square = document.createElement('mydiv'); //creating square for animation
    square.className = 'square';
    
    border.appendChild(square); //adding square to border
    //⌄⌄⌄ adding animation to document
    document.body.appendChild(border);
    
    //⌄⌄⌄ adding html of animation to list of html strings
    if (!window.hasOwnProperty('htmlstringlist'))
    {
        window.htmlstringlist = ["user = " + username + ";", gui_elements]; //second element is being returned by index function in views.py
    }
    
    window.htmlstringlist.push(border.outerHTML.toString());
  
    fullHtml = window.htmlstringlist.join(' '); //converting html list to one html string
    
    fullHtmlDict = {"function": "gui_change", "instructions": fullHtml};
    SendBack(JSON.stringify(fullHtmlDict)); //send back to subscriber to update user's mongodb. First, sends it to the ZMQChannels receive method (where arg = fullHtml) and then from there to the server.py func_receive function
                            
    document.getElementById('ctxmenu').remove(); //removes right-click menu from document
};

function removeBasicAnimation()
{
    var ctxMenu = document.getElementById("border_id"); //get animation html element
    if (ctxMenu) //if an animation is on the webpage, delete it
    {
        if (!window.hasOwnProperty('htmlstringlist'))
        {
            window.htmlstringlist = ["user = " + username + ";", gui_elements]; //second element is being returned by index function in views.py
        }
        fullHtml = window.htmlstringlist.join(' ');
        if (window.htmlstringlist.length > 1)
        {
            
            length = window.htmlstringlist.length;
            // finds last index of mydiv element in last element of htmlstringlist
            lastIndex = window.htmlstringlist[length-1].lastIndexOf(String.raw`<mydiv id="border_id"`);
            
            console.log(lastIndex);
            
            //reintializing last element of htmlstringlist with a substring that doesn't contain the last mydiv element
            window.htmlstringlist[length-1] = window.htmlstringlist[length-1].substring(0,lastIndex);
            
            if (!window.htmlstringlist[length-1]) //if last element of htmlstringlist is empty
            {
                //get rid of last element in htmlstringlist and log it to the console
                const elem = window.htmlstringlist.pop();
                console.log("elem = ",elem);
            }
        }
        //parsing from a list to a string where each element in the string is separated by a space
        fullHtml = window.htmlstringlist.join(' ');
        console.log(fullHtml);
        fullHtmlDict = {"function": "gui_change", "instructions": fullHtml};
        SendBack(JSON.stringify(fullHtmlDict)); //sending updated html to the subscriber in server.py
        ctxMenu.parentNode.removeChild(ctxMenu);
    }
    document.getElementById('ctxmenu').remove(); //removes right-click menu from document
};

/// Pause all animations
function PauseAnimations()
{
    // Get all elements with the .square class
    var squareElements = document.querySelectorAll('.square');

    // Loop through each square element and set animation-play-state to "paused"
    for (var i = 0; i < squareElements.length; i++)
    {
          var squareElement = squareElements[i];
          squareElement.style.animationPlayState = 'paused';
    }
}

/// Resume all animations
function ResumeAnimations()
{
    // Get all elements with the .square class
    var squareElements = document.querySelectorAll('.square');

    // Loop through each square element and set animation-play-state to "running"
    for (var i = 0; i < squareElements.length; i++)
    {
        var squareElement = squareElements[i];
        squareElement.style.animationPlayState = 'running';
    }
}

function describeExperiment(Experiment)
{
    ExperimentInfo = functionDict[Experiment];
    var ExperimentElement = document.getElementById(Experiment);
    if (ExperimentElement.getAttribute("expanded") === null)
    {
        ExperimentElement.setAttribute("expanded", true);
        
        ExperimentElement.innerHTML += '\n' + '<form>';
        let count = 0;
        for (param in ExperimentInfo["params"])
        {
            let ExperimentInfoParamId = param + count;
            ExperimentElement.innerHTML += '\n' + String.raw`<div class="form-group">`;
            ExperimentElement.innerHTML += '\n' + String.raw`<label for="` + ExperimentInfoParamId + String.raw`">` + param + String.raw`label</label>`;
            ExperimentElement.innerHTML += '\n' + String.raw`<input type="text" class="form-control" id="` + ExperimentInfoParamId + String.raw`" placeholder="` + ExperimentInfo["params"][param]["default"]  + String.raw`">`;
            ExperimentElement.innerHTML += String.raw`</div>`;
                            
            count++;
        }
        ExperimentElement.innerHTML += '\n' + '</form>';
    }
    else
    {
        let describeExperimentStr = "describeExperiment('" + Experiment + "')";
        let temp = String.raw
        `
        <span onclick = "describeExperimentStr" onmouseover="this.style.cursor='pointer'" onmouseleave="this.style.cursor='default'">
            &#43;
        </span>
        `;
        temp = temp.replaceAll("ExperimentName", Experiment); //replace all instances of ExperimentName w/ Experiment variable
        temp = temp.replace("describeExperimentStr", describeExperimentStr);
        
        ExperimentElement.innerHTML = temp;
        ExperimentElement.removeAttribute("expanded");
    }
}

// this function fires when the user clicks the x on the top-left corner of the voltage menu
function closeExperimentWindow()
{
    var voltageChannelMenu = document.getElementById("ctxmenu_voltage");
    if (voltageChannelMenu)
    {
        voltageChannelMenu.parentNode.removeChild(voltageChannelMenu);
    }
}

function AddExperiment()
{
    if (!window.ExperimentAdded)
    {
        window.ExperimentAdded = true;
        //var jsonPretty = JSON.stringify(functionDict, null, 2);
        //console.log(jsonPretty);
        
        let ExperimentMenu = document.createElement("div"); //create a 'ul' element for ExperimentMenu
        ExperimentMenu.setAttribute("class", "col-sm"); // MARK: - Dragging only seems to work with col-sm elements -
        ExperimentMenu.setAttribute("id", "ExperimentMenu");
        ExperimentMenu.setAttribute("draggable", true);
//        ExperimentMenu.innerHTML +=
//        String.raw
//        `
//        <div class="row">
//            <div class="col-sm" align = "left">
//                <a href="javascript:void(0)" class="closebtn" onclick="closeWindow(); window.ExperimentAdded = false;" style = "color:red;">&times;</a>
//            </div>
//        </div>
//        <br/>
//        `.replace("closeWindow()", "closeWindow('" + ExperimentMenu.id + "')");
        
        for (Experiment in functionDict)
        {
            let describeExperimentStr = "describeExperiment('" + Experiment + "')";
            let temp = String.raw
            `
            <div class="row">
                <div class="col-sm" align = "left">
                    <a href="javascript:void(0)" class="closebtn" onclick="closeWindow(); window.ExperimentAdded = false;" style = "color:red;">&times;</a>
                </div>
                <div class="col-sm" align = "right">
                    ExperimentName
                </div>
                <div class="col-sm" align = "left" id = ExperimentName>
                    <span onclick = "describeExperimentStr" onmouseover="this.style.cursor='pointer'" onmouseleave="this.style.cursor='default'">
                        &#43;
                    </span>
                </div>
            </div>
            `.replace("closeWindow()", "closeWindow('" + ExperimentMenu.id + "')");
            
            temp = temp.replaceAll("ExperimentName", Experiment); //replace all instances of ExperimentName w/ Experiment variable
            temp = temp.replace("describeExperimentStr", describeExperimentStr);
            
            ExperimentMenu.innerHTML += temp;
        }
        ExperimentMenu.addEventListener('dragstart', startDrag, true);
        ExperimentMenu.addEventListener('dragend', endDrag, true);
        document.body.appendChild(ExperimentMenu);
    }
    
    //Structure of functionDict:
    //{
    //    "Experiment": {
    //        "params": {
    //          "param1": {
    //            "type": "the type of param1",
    //            "default": "the default value of param1",
    //            "info": "the description of param1"
    //          },
    //           ...
    //        },
    //        "description": "This Experiment does a 729 Shelving Test.",
    //        "other_metadata": []
    //      },
    //    ...
    //}
    
}

function AddSelectedExperiments()
{
    for (Experiment in functionDict)
    {
        let ExperimentIdString = "flexCheckDefault" + Experiment;
        let ExperimentElem = document.getElementById(ExperimentIdString);
        if (ExperimentElem && ExperimentElem.checked)
        {
            let elem = document.createElement("div"); //create a 'div' element for menu
            elem.innerHTML = Experiment;
            elem.setAttribute("class", "col-sm-4");
            elem.setAttribute("name", Experiment);
            elem.setAttribute("draggable", "true");
            elem.setAttribute("style", "border:1px solid black; margin:5px;");
            elem.setAttribute("onmouseover", "this.style.cursor='pointer'");
            elem.setAttribute("onmouseleave", "this.style.cursor='default'");
            elem.setAttribute("ondragstart", "startDrag(event)");
            elem.setAttribute("ondragend", "endDrag(event)");
            elem.setAttribute("align", "center");
            console.log(elem);
            document.getElementById("whole_html").appendChild(elem);
        }
    }
    
}

function SearchForExperiment()
{
    let userInput = document.querySelector('#SearchForExperimentInput').value;
    let ExperimentSearchBar = document.getElementById("add-experiment-search-bar");
    let SubmitString =
    String.raw
    `
        <button type="button" class="btn btn-success" name = "SubmitExperiments" onclick="AddSelectedExperiments()">Submit</button>
    `;
    let checkedElemFound = false;
    for (Experiment in functionDict)
    {
        let NameString = "[name='Experiment']".replace("Experiment", Experiment);
        if (element = ExperimentSearchBar.querySelector(NameString))
        {
            ExperimentSearchBar.removeChild(element);
        }
        if (Experiment.includes(userInput))
        {
            ExperimentSearchBar.innerHTML +=
            String.raw
            `
            <div class="col-sm" align = "left" name = "Experiment">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="flexCheckDefaultExperiment" onclick = "console.log(this.checked);">
                    <label class="form-check-label" for="flexCheckDefaultExperiment">
                        Experiment
                    </label>
                </div>
            </div>
            `.replaceAll("Experiment", Experiment);
            checkedElemFound = true;
        }
    }
    
    let SubmitNameString = "[name='SubmitExperiments']";
    if (element = ExperimentSearchBar.querySelector(SubmitNameString))
    {
        ExperimentSearchBar.removeChild(element);
    }
    if (checkedElemFound)
    {
        ExperimentSearchBar.innerHTML += SubmitString;
    }

    document.querySelector('#SearchForExperimentInput').value = userInput;
}

/// Gets the `number` checkbox (e.g. 0, 1, 2, ..., or 15) and checks or unchecks all of them
/// for each voltage channel window on the DOM. `checked` is either true (check) or false (uncheck)
function checkVoltageChannelBoxes(number, checked)
{
    var channel_box_id = "[id='flexCheckDefault" + number + "']";
    var channel_boxes = document.querySelectorAll(channel_box_id); //getting all tick boxes for voltage channel 'i'
    for (var j = 0; j < channel_boxes.length; j++)
    {
        channel_boxes[j].checked = checked;
    }
    
}

// this function fires when the user clicks the x on the top-left corner
function closeWindow(id)
{
    var element = document.getElementById(id);
    if (element)
    {
        element.parentNode.removeChild(element);
    }
}

function SetVoltageChannels(top, left)
{
    let menu = document.createElement("div"); //create a 'div' element for menu
    menu.id = "ctxmenu_voltage"; //set id of menu
    menu.name = "menu";
    menu.style.top = (top)+"px";    //y-position of menu
    menu.style.left = (left)+"px";   //x-position of menu
    
    menu.draggable = true; //make menu draggable
    //⌄⌄⌄ behaviour when user starts dragging this element
    menu.addEventListener('dragstart', startDrag, true);
    //⌄⌄⌄ behaviour when user stops dragging this element
    menu.addEventListener('dragend', endDrag, true);
    
    menu.innerHTML = //This is the html string for the voltage channels checkbox menu, it uses bootstrap grid
    String.raw`
    <div class="container-fluid pt-1 pl-1">
        <div class="row">
            <div class="col-sm" align = "left">
                <a href="javascript:void(0)" class="closebtn" onclick="closeWindow()" style = "color:red;">&times;</a>
            </div>
        </div>
        </br>
        <div class="row">
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault0" onclick = "checkVoltageChannelBoxes(0, this.checked);">
                <label class="form-check-label" for="flexCheckDefault0">
                Voltage channel 0
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault1" onclick = "checkVoltageChannelBoxes(1, this.checked);">
                <label class="form-check-label" for="flexCheckDefault1">
                Voltage channel 1
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault2" onclick = "checkVoltageChannelBoxes(2, this.checked);">
                <label class="form-check-label" for="flexCheckDefault2">
                Voltage channel 2
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault3" onclick = "checkVoltageChannelBoxes(3, this.checked);">
                <label class="form-check-label" for="flexCheckDefault3">
                Voltage channel 3
                </label>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault4" onclick = "checkVoltageChannelBoxes(4, this.checked);">
                <label class="form-check-label" for="flexCheckDefault4">
                Voltage channel 4
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault5" onclick = "checkVoltageChannelBoxes(5, this.checked);">
                <label class="form-check-label" for="flexCheckDefault5">
                Voltage channel 5
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault6" onclick = "checkVoltageChannelBoxes(6, this.checked);">
                <label class="form-check-label" for="flexCheckDefault6">
                Voltage channel 6
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault7" onclick = "checkVoltageChannelBoxes(7, this.checked);">
                <label class="form-check-label" for="flexCheckDefault7">
                Voltage channel 7
                </label>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault8" onclick = "checkVoltageChannelBoxes(8, this.checked);">
                <label class="form-check-label" for="flexCheckDefault8">
                Voltage channel 8
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault9" onclick = "checkVoltageChannelBoxes(9, this.checked);">
                <label class="form-check-label" for="flexCheckDefault9">
                Voltage channel 9
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault10" onclick = "checkVoltageChannelBoxes(10, this.checked);">
                <label class="form-check-label" for="flexCheckDefault10">
                Voltage channel 10
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault11" onclick = "checkVoltageChannelBoxes(11, this.checked);">
                <label class="form-check-label" for="flexCheckDefault11">
                Voltage channel 11
                </label>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault12" onclick = "checkVoltageChannelBoxes(12, this.checked);">
                <label class="form-check-label" for="flexCheckDefault12">
                Voltage channel 12
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault13" onclick = "checkVoltageChannelBoxes(13, this.checked);">
                <label class="form-check-label" for="flexCheckDefault13">
                Voltage channel 13
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault14" onclick = "checkVoltageChannelBoxes(14, this.checked);">
                <label class="form-check-label" for="flexCheckDefault14">
                Voltage channel 14
                </label>
                </div>
            </div>
            <div class="col-sm" align = "center">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault15" onclick = "checkVoltageChannelBoxes(15, this.checked);">
                <label class="form-check-label" for="flexCheckDefault15">
                Voltage channel 15
                </label>
                </div>
            </div>
        </div>
    
    <br>
    <button type="button" class="btn btn-success" onclick="SubmitVoltages()">Submit</button>
    </div>
    `.replace("closeWindow()", "closeWindow('" + menu.id + "')");

    document.body.appendChild(menu); //add menu to document body
    
    for (let i = 0; i < 16; i++)
    {
        var channel_box_id = "[id='flexCheckDefault" + i + "']";
        var channel_boxes = document.querySelectorAll(channel_box_id); //getting all tick boxes for voltage channel 'i'
        for (var j = 0; j < channel_boxes.length; j++)
        {
            channel_boxes[j].checked = window.activatedChannels[i];
        }
    }
}

/// This is what happens when the user clicks `Submit` on the voltage channel menu
function SubmitVoltages()
{
    //First, activate the channels that are checked
    for (let i = 0; i < 16; i++)
    {
        var x = document.getElementById("flexCheckDefault" + i); //get checkbox i
        window.activatedChannels[i] = x.checked; //channel i is activated if x.checked is true, else channel i is deactivated
    }
    //Now, delete all the voltage channel menus from the screen
    var voltage_channel_menu_id = "[id='ctxmenu_voltage']";
    var voltage_channel_menus = document.querySelectorAll(voltage_channel_menu_id); //gets ALL voltage channel menus

    //remove right-click menu if there's one or more menu windows on the webpage (ctxMenu)
    if (voltage_channel_menus)
    {
        for (var j = 0; j < voltage_channel_menus.length; j++)
        {
            voltage_channel_menus[j].parentNode.removeChild(voltage_channel_menus[j]);
        }
    }
    console.log(window.activatedChannels)
    SetVoltageDict = {"function": "gui_change", "instructions": ["changeVoltageChannels", window.activatedChannels]}
    
    SendBack(JSON.stringify(SetVoltageDict)); //store the updated activatedChannels in the user's mongodb
    
}
            
//⌄⌄⌄ Fires when user right-clicks on page ⌄⌄⌄
document.addEventListener("contextmenu", function (e) {
    
    var top = e.clientY;
    var left = e.clientX;
    console.log(top,left);
    e.preventDefault(); //prevent default right-click behaviour
    let menu = document.createElement("mydiv"); //create a 'mydiv' element for menu
    menu.id = "ctxmenu"; //set id of menu
    menu.style.top = (e.clientY)+"px";    //y-position of menu
    menu.style.left = (e.clientX)+"px";   //x-position of menu
    
    menu.draggable = true; //make menu draggable
    //⌄⌄⌄ behaviour when user starts dragging this element
    menu.addEventListener('dragstart', startDrag, true);
    //⌄⌄⌄ behaviour when user stops dragging this element
    menu.addEventListener('dragend', endDrag, true);
    
    //⌄⌄⌄ Can add more elements to the right click menu in the String.raw below ⌄⌄⌄
    menu.innerHTML =
    String.raw`
    <p onclick = "basicAnimation()">Add Basic Animation</p>
    <p onclick = "removeBasicAnimation()">Remove Basic Animation</p>
    <p onclick = "Start()">Start</p>
    <p onclick = "Stop()">Stop</p>
    <p onclick = "SendBack('{&quot;function&quot;: &quot;signal&quot;, &quot;instructions&quot;: &quot;Hi friend!!&quot;}')">Signal</p>
    <p onclick = "PauseAnimations()">Pause Animations</p>
    <p onclick = "ResumeAnimations()">Resume Animations</p>
    <p onclick = "AddExperiment()"> Add Experiment</p>
    `;
    
    let setVoltageChannelsButton = document.createElement("p"); //creating a separate element for setting voltages
    setVoltageChannelsButton.textContent = "Set Voltage Channels";
    
    setVoltageChannelsButton.addEventListener("click", function() {
        SetVoltageChannels(top, left);
    });

    menu.appendChild(setVoltageChannelsButton); //for some reason, this needs to be added separately...

    document.body.appendChild(menu); //add menu to document body
    
}, false); //change to true to make it fire relatively sooner (if I understand the docs correctly...)

//⌄⌄⌄ 1 click on the webpage corresponds to 1 menu that disappears from the webpage
document.addEventListener("click",function(event){
    
    var ctxMenu = document.getElementById("ctxmenu"); //true if a menu is on the webpage, false if not
    //remove right-click menu if there's one or more menu windows on the webpage (ctxMenu)
    if (ctxMenu)
    {
        ctxMenu.parentNode.removeChild(ctxMenu); //remove 1 menu from webpage
        return;
    }

}, false);

function Start()
{
    var count = 0;
    const interval = 100;
    if (!window.hasOwnProperty('started'))
    {
        window.started = false;
    }
    if (!window.started)
    {
        window.chatSocket = new WebSocket(
                    'ws://'
                    + window.location.host
                   + '/ws/members/'
                );
        window.started = true;
    }
        
    window.chatSocket.onclose = function(e) {
        //Reference: https://stackoverflow.com/a/61283792/18255427
        let specificStatusCodeMappings = {
            '1000': 'Normal Closure',
            '1001': 'Going Away',
            '1002': 'Protocol Error',
            '1003': 'Unsupported Data',
            '1004': '(For future)',
            '1005': 'No Status Received',
            '1006': 'Abnormal Closure',
            '1007': 'Invalid frame payload data',
            '1008': 'Policy Violation',
            '1009': 'Message too big',
            '1010': 'Missing Extension',
            '1011': 'Internal Error',
            '1012': 'Service Restart',
            '1013': 'Try Again Later',
            '1014': 'Bad Gateway',
            '1015': 'TLS Handshake'
        };
        
        console.log(specificStatusCodeMappings[e.code]); //reports closure status
    };

    //⌄⌄⌄ Fires when data is received
    window.chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);

        data = data.event.text;
                            
        if (data[0] == 'MAXBOX' && document.getElementById("voltages") !== null)
        {
            var voltage_x_vals = []; //line-graph x-coordinates
            
            if (!window.hasOwnProperty('lowVoltageBin'))
            {
                window.lowVoltageBin = 0; //lower x-value for voltage line graph
            }
            
            if (!window.hasOwnProperty('highVoltageBin'))
            {
                window.highVoltageBin = 0; //upper x-value for voltage line graph
            }
            
            for (let i = window.lowVoltageBin; i <= window.highVoltageBin; i++)
            {
                voltage_x_vals.push(i);
            }
            
            var curr_data = data[1];
            var max_length = 100; //change this to make x-range larger for voltage channels
            var voltage_channel_data = [];
            
            if (window.highVoltageBin > max_length - 1)
            {
                //move graphs to right
                window.highVoltageBin++;
                window.lowVoltageBin++;
            }
            else
            {
                //increase upper limit until the x-range has reached max_length
                window.highVoltageBin++;
            }
            
            if (!window.hasOwnProperty('activatedChannels'))
            {
                window.activatedChannels = Array(16).fill(true); //by default all channels are activated
                if (channelsActivated.length == 16)
                {
                    window.activatedChannels = channelsActivated;
                }
            }
            
            //first check if there are any activated channels:
            if (window.activatedChannels.every(element => element === false))
            {
                document.getElementById("voltages").innerHTML = "";
                return;
            }
            
            var voltage_channel_counter = 0; //number of active channels, not always equal to 16
            //loop over 16 channels;
            for (let i = 0; i < 16; i++)
            {
                if (window.activatedChannels[i])
                {
                    if (!window.hasOwnProperty('voltageChannelVals'))
                    {
                        window.voltageChannelVals = Array(16); //2d array of 16 channels and their corresponding values
                    }
                    if (window.voltageChannelVals[i] == undefined) //list is empty
                    {
                        window.voltageChannelVals[i] = [curr_data[i]];
                    }
                    else if (window.voltageChannelVals[i].length >= max_length) //move graph to right
                    {
                        window.voltageChannelVals[i].splice(0,1); //get rid of first element
                        window.voltageChannelVals[i].push(curr_data[i]); //add new value to end of list for this channel
                    }
                    else //keep adding data to i'th channel
                    {
                        window.voltageChannelVals[i].push(curr_data[i]); //add new value to end of list for this channel
                    }
                    var temp_trace = {};
                    if (!voltage_channel_counter)
                    {
                        temp_trace =
                        {
                            x: voltage_x_vals,
                            y: window.voltageChannelVals[i],
                            name: "voltage channel " + i,
                            type: 'scatter'
                        };
                        voltage_channel_counter++;
                    }
                    else
                    {
                        temp_trace =
                        {
                            x: voltage_x_vals,
                            y: window.voltageChannelVals[i],
                            xaxis: 'x' + (voltage_channel_counter + 1),
                            yaxis: 'y' + (voltage_channel_counter + 1),
                            name: "voltage channel " + i,
                            type: 'scatter'
                        };
                        voltage_channel_counter++;
                    }
                    voltage_channel_data.push(temp_trace);
                }
            }
            
            var layout = {
              grid: {rows: 8, columns: 2, pattern: 'independent'}, autosize: false, margin: {
                  l: 40,
                  r: 40,
                  b: -10,
                  t: 50,
                  pad: 4
              },
              height: 2000,
              width: 1000,
              roworder: 'bottom to top'
            };
            
            Plotly.newPlot('voltages', voltage_channel_data, layout);
            return;
        }
        //else, this could be the result of "Set Output"
        //else if (typeof data.event.text === "undefined" && typeof data.event.send_freq_chan_ampl_phase_to_dds_zmq !== "undefined")
        //{
        //    var result = data.event.send_freq_chan_ampl_phase_to_dds_zmq;
        //    console.log(result);
        //    if (result) //if successfully written, display a green checkmark for 2 seconds
        //    {
        //        document.getElementById("dropdownMenuButtonSetFreqAmplChanPhaseOutput").innerHTML =
        //        String.raw
        //        `
        //        <font size="72 px">&#9989</font>
        //        `;
        //    }
        //    else //else, display a red X for 2 seconds
        //    {
        //        document.getElementById("dropdownMenuButtonSetFreqAmplChanPhaseOutput").innerHTML =
        //        String.raw
        //        `
        //        <font size="72 px">&#10060</font>
        //        `;
        //    }
        //
        //
        //    setTimeout(() => {  document.getElementById("dropdownMenuButtonSetFreqAmplChanPhaseOutput").innerHTML = "Set Output"; }, 2000);
        //
        //    return;
        //}
        //
        ////else, this could be the result of "Read Temperature"
        //else if (typeof data.event.text === "undefined" && typeof data.event.send_chan_read_temp_to_dds_zmq !== "undefined")
        //{
        //    var result = data.event.send_chan_read_temp_to_dds_zmq;
        //    var channel = data.event.channel
        //    console.log(result);
        //    document.getElementById("dropdownMenuButtonChanOutput").innerHTML = "Temperature at Channel " + channel + " = " +  result;
        //
        //
        //    setTimeout(() => {  document.getElementById("dropdownMenuButtonChanOutput").innerHTML = "Read Temperature"; }, 2000);
        //
        //    return;
        //}

        //⌄⌄⌄ else it's the heat-map-line-graph data, handled below ⌄⌄⌄
        
        else if (data[0] == 'CAMERA' && document.getElementById("heat-map-line-graph-show") !== null)
        {
            var startTime = parseFloat(data[2])*1000;
                                    
            var endTime = new Date().getTime();
            
            var timeDiff = (endTime-startTime)/1000;
            
            // ⌄⌄⌄ Update the 'Time Difference (seconds):' text box
            if (document.querySelector('#timediff'))
            {
                document.querySelector('#timediff').value = timeDiff; //re-assign value displayed in text box
            }
            
            //⌄⌄⌄ parsing data, first value is line graph value, rest are camera pixel values
            Data = data[1];
            
            if (!window.hasOwnProperty('lineVals')) //stores y-coordinates of line plot
            {
                window.lineVals = [];
            }
            window.lineVals.push(Data[0]); //y-axis line graph values
            if (window.lineVals.length > interval)
            {
                window.lineVals.splice(0,1);
            }
            
            if (!window.hasOwnProperty('minlineVal'))
            {
                window.minlineVal = false; //y-min line graph
            }
            
            if (!window.hasOwnProperty('maxlineVal'))
            {
                window.maxlineVal = false; //y-max line graph
            }
            
            if (!window.minlineVal && !window.maxlineVal)
            {
                window.minlineVal = Data[0];
                window.maxlineVal = Data[0];
            }
            
            //Below denotes the auto adjusting of the line graph y-range
            //Basically, this makes the y-range the min and max of the last
            //`interval` numbers, in this case, interval = 100
            
            let lineValsMin = Math.min(...window.lineVals);
            if (window.minlineVal < lineValsMin)
            {
                window.minlineVal = lineValsMin;
            }
            else if (window.minlineVal > lineValsMin)
            {
                window.minlineVal = Data[0];
            }
            
            let lineValsMax = Math.max(...window.lineVals);
            if (window.maxlineVal > lineValsMax)
            {
                window.maxlineVal = lineValsMax;
            }
            else if (window.maxlineVal < lineValsMax)
            {
                window.maxlineVal = Data[0];
            }
            //auto-adjusting concluded ;-)
            
            newArr = []; //Stores Camera pixels as a 2d array
            Data.splice(0,1);
            while(Data.length) newArr.push(Data.splice(0,11));
            var my_plot = //heatmap plot
            {
                z : newArr,
                type: 'heatmap',
                // opacity: 0.8,
                zmin: 407,
                zmax: 1518,
                showlegend: false,
                showlegend: false,
                xaxis: {visible: false},
                showscale: false,
                //colorbar: {showlegend: false, xaxis: {visible: false},showscale: false, orientation: 'h', ticklabelposition: "right"}
            };
            
            if (!window.hasOwnProperty('lowEnd'))
            {
                window.lowEnd = 0; //lower x-value for line graph
            }
            if (!window.hasOwnProperty('highEnd'))
            {
                window.highEnd = 0; //upper x-value for line graph
            }
            
            var list = []; //line-graph x-coordinates
            for (var i = window.lowEnd; i <= window.highEnd; i++) {
                list.push(i);
            }
            
            var next_plot = //line graph
            {
                x: list,
                y: window.lineVals,
                type: 'scatter',
                xaxis: 'x2',
                yaxis: 'y2',
            };
            
            var layout = {
                //⌄⌄⌄ heat-map subplot
                xaxis: {domain: [0, 0.3], "visible": false}, //heat map takes up 30% of screen
                yaxis: {"visible": false},
                
                //sets the y axis of the line graph subplot
                yaxis2: {anchor: 'x2', range: [ window.minlineVal, window.maxlineVal]},
                
                xaxis2: {domain: [0.35, 1], range: list}, //how much of screen the line graph subplot takes up, here it takes up 65%
                
                //⌄⌄⌄ 1 row with 1 column for heat map and 1 column for line graph
                grid: {rows: 1, columns: 2, pattern: 'independent'},
                
                margin: {
                    l: 40,
                    r: 40,
                    b: -10,
                    t: 50,
                    pad: 4
                }
            };
            Plotly.newPlot('heat-map-line-graph-show', [my_plot, next_plot], layout);
            if (window.highEnd < 99) //increase x-axis upper bound by 1 if it's less than 99, can change '99' to whatever you like
            {
                window.highEnd++;
            }
            else    //else increase the x-axis lower and upper bounds by 1
            {
                window.lowEnd++;
                window.highEnd++;
            }
        }
    };
}

//Stop data streaming, called when user clicks 'Stop' ⌄⌄⌄
function Stop()
{
    window.chatSocket.close();
    window.started = false;
}

//Send a message back to subscriber, called when user clicks 'Signal' ⌄⌄⌄
function SendBack(arg = '{"function": null, "instructions": null}')
{
    if (window.chatSocket.readyState !== WebSocket.OPEN) //if window.chatSocket is not connected, connect it
    {
        window.chatSocket = new WebSocket(
                    'ws://'
                    + window.location.host
                   + '/ws/members/'
                ); //first start up the chat socket
        
//        https://dev.to/ndrbrt/wait-for-the-websocket-connection-to-be-open-before-sending-a-message-1h12
        const waitForOpenConnection = (socket) =>
        {
            return new Promise((resolve, reject) => {
                const maxNumberOfAttempts = 10
                const intervalTime = 200 //ms

                let currentAttempt = 0
                const interval = setInterval(() => {
                    if (currentAttempt > maxNumberOfAttempts - 1) {
                        clearInterval(interval)
                        reject(new Error('Maximum number of attempts exceeded'))
                    } else if (socket.readyState === socket.OPEN) {
                        clearInterval(interval)
                        resolve()
                    }
                    currentAttempt++
                }, intervalTime)
            });
        };
        
        const sendMessage = async (socket, msg) =>
        {
            if (socket.readyState !== socket.OPEN) {
                try {
                    await waitForOpenConnection(socket)
                    socket.send(msg)
                } catch (err) { console.error(err) }
            } else {
                socket.send(msg)
            }
        };
        
        sendMessage(window.chatSocket, arg);
//        window.chatSocket.onopen = () => {window.chatSocket.send(arg);} //send it
        window.started = true; //flag to denote that chat socket is up and running
    }
    else //if it is, just send back the data stored in the variable 'arg' to the consumers.py ZMQChannels.receive method
    {
        window.chatSocket.send(arg); //send it
    }
}

function SendChan()
{
    var chanVal = document.getElementById("myChannelReadTempRange").value;
    
    console.log(chanVal);
    var running = window.started;

    ReadTemperatureDict = {"function": "exec_exp", "instructions": ["read_temperature", chanVal]}
    //SendBack(JSON.stringify(ReadTemperatureDict));
    
    CloseChanSetter();
    
    if (!running)
    {
        Start();
    }
}

function SendFreqAmplChanPhase()
{
    var freqVal = document.getElementById("myFrequencyRange").value;
    var ampVal = document.getElementById("myAmplitudeRange").value;
    var chanVal = document.getElementById("myChannelRange").value;
    var phaseVal = document.getElementById("myPhaseRange").value;
    var profVal = document.getElementById("myProfileRange").value;
    
    console.log(freqVal, ampVal, chanVal, phaseVal, profVal);
    var running = window.started;

    SetOutputDict = {"function": "set_values", "instructions": ["set_output", freqVal, ampVal, chanVal, phaseVal, profVal]}
    //SendBack(JSON.stringify(SetOutputDict));
    
    CloseFreqAmplChanPhaseSetter();
    
    if (!running)
    {
        Start();
    }
}

function CloseChanSetter()
{
    let elem = document.getElementById("dropdownMenuButtonChanOutput");
    elem.innerHTML =
    String.raw`
    <button type="button" class="btn btn-info" onclick="ChannelSetter();">
        Read Temperature
    </button>
    `;
    elem.style.backgroundColor = "white";
    elem.draggable = true;
}
            
function ChannelSetter()
{
    const dropdownMenuButtonChanOutput_elem = document.getElementById("dropdownMenuButtonChanOutput")
    dropdownMenuButtonChanOutput_elem.innerHTML =
    String.raw
    `
    <div class="row">
        <div class="col-sm" align = "left">
            <a href="javascript:void(0)" class="closebtn" onclick="CloseChanSetter()" style = "color:red;">&times;</a>
        </div>
    </div>
    <br/>
    <div class="row">
        <div class="col-sm" align = "center">
            <div class="slidecontainer">
                <input type="range" min="0" max="3" value="0" step = "1" class="slider" id="myChannelReadTempRange">
                <p>Channel:
                    <span id="ChannelReadTempDemo">
                    </span>
                </p>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-sm" align = "center">
            <button type="button" class="btn btn-success" onclick="SendChan()">
                Read Now!
            </button>
        </div>
    </div>
    `;
    
    //The following adds event listeners to the slider to make the
    //`dropdownMenuButtonChanOutput_elem` draggable only when the mouse
    //is NOT on the slider
    let myChannelReadTempRange = document.getElementById("myChannelReadTempRange");
    myChannelReadTempRange.addEventListener("mouseover", () =>
    {
        dropdownMenuButtonChanOutput_elem.setAttribute("draggable", false);
    });
    myChannelReadTempRange.addEventListener("mouseleave", () =>
    {
        dropdownMenuButtonChanOutput_elem.setAttribute("draggable", true);
    });
    //end of adding slider event listeners ;-)
    
    dropdownMenuButtonChanOutput_elem.backgroundColor = "white"; //or whatever color you prefer.
    
    var channelSlider = document.getElementById("myChannelReadTempRange");
    if (!window.hasOwnProperty('channelValue'))
    {
        window.channelValue = 0;
    }
    channelSlider.value = window.channelValue;
    var channelOutput = document.getElementById("ChannelReadTempDemo");
    channelOutput.innerHTML = channelSlider.value;

    channelSlider.oninput = function()
    {
        channelOutput.innerHTML = this.value;
        window.channelValue = this.value;
    }
}

function CloseFreqAmplChanPhaseSetter()
{
    let elem = document.getElementById("dropdownMenuButtonSetFreqAmplChanPhaseOutput");
    elem.innerHTML =
    String.raw`
    <button type="button" class="btn btn-info" onclick="FreqAmplChanPhaseSetter();">
        Set Output
    </button>
    `;
    elem.style.backgroundColor = "white";
    elem.draggable = true;
}

function FreqAmplChanPhaseSetter()
{
    const dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem = document.getElementById("dropdownMenuButtonSetFreqAmplChanPhaseOutput");
    
    dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.innerHTML =
    String.raw
    `
    <div class="row">
        <div class="col-sm" align = "left">
            <a href="javascript:void(0)" class="closebtn" onclick="CloseFreqAmplChanPhaseSetter()" style = "color:red;">&times;</a>
        </div>
    </div>
    <br/>
    <div class="row">
        <div class="col-sm" align = "center">
            <div class="slidecontainer">
                <input type="range" min="0" max="1" value="0.5" step = "0.1" class="slider" id="myAmplitudeRange">
                <p>Amplitude:
                    <span id="amplitudeDemo">
                    </span>
                </p>
            </div>
        </div>
    
        <div class="col-sm" align = "center">
            <div class="slidecontainer">
                <input type="range" min="1" max="100" value="50" step = "1" class="slider" id="myFrequencyRange">
                <p>Frequency:
                    <span id="frequencyDemo">
                    </span>
                </p>
            </div>
        </div>
    
        <div class="col-sm" align = "center">
            <div class="slidecontainer">
                <input type="range" min="0" max="3" value="0" step = "1" class="slider" id="myChannelRange">
                <p>Channel:
                    <span id="channelDemo">
                    </span>
                </p>
            </div>
        </div>
    </div>
    
    <br/> <br/>
    
    <div class="row">
        <div class="col-sm" align = "center">
            <div class="slidecontainer">
                <input type="range" min="0" max="360" value="0" step = "0.1" class="slider" id="myPhaseRange">
                <p>Phase:
                    <span id="phaseDemo">
                    </span>
                </p>
            </div>
        </div>
    
        <div class="col-sm" align = "center">
            <div class="slidecontainer">
                <input type="range" min="0" max="7" value="0" step = "1" class="slider" id="myProfileRange">
                <p>Profile:
                    <span id="profileDemo">
                    </span>
                </p>
            </div>
        </div>
    </div>
    
    <br/>
    
    <div class="row">
        <div class="col-sm" align = "center">
            <button type="button" class="btn btn-success" onclick="SendFreqAmplChanPhase()">Send All!</button>
        </div>
    </div>
    `;
    
    //The following adds event listeners to the sliders to make the
    //`dropdownMenuButtonSetFreqAmplChanPhaseOutput` draggable only when the mouse
    //is NOT on a slider
    let myAmplitudeRange = document.getElementById("myAmplitudeRange");
    myAmplitudeRange.addEventListener("mouseover", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", false);
    });
    myAmplitudeRange.addEventListener("mouseleave", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", true);
    });
    
    let myFrequencyRange = document.getElementById("myFrequencyRange");
    myFrequencyRange.addEventListener("mouseover", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", false);
    });
    myFrequencyRange.addEventListener("mouseleave", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", true);
    });
    
    let myChannelRange = document.getElementById("myChannelRange");
    myChannelRange.addEventListener("mouseover", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", false);
    });
    myChannelRange.addEventListener("mouseleave", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", true);
    });
    
    let myPhaseRange = document.getElementById("myPhaseRange");
    myPhaseRange.addEventListener("mouseover", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", false);
    });
    myPhaseRange.addEventListener("mouseleave", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", true);
    });
    
    let myProfileRange = document.getElementById("myProfileRange");
    myProfileRange.addEventListener("mouseover", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", false);
    });
    myProfileRange.addEventListener("mouseleave", () =>
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.setAttribute("draggable", true);
    });
    //end of adding slider event listeners ;-)

    dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.style.backgroundColor = "white"; //or whatever color you prefer.

    var amplSlider = document.getElementById("myAmplitudeRange");
    if (!window.hasOwnProperty('amplitudeValue'))
    {
        window.amplitudeValue = 0.5;
    }
    amplSlider.value = window.amplitudeValue;
    var amplOutput = document.getElementById("amplitudeDemo");
    amplOutput.innerHTML = amplSlider.value;

    amplSlider.oninput = function()
    {
        amplOutput.innerHTML = this.value;
        window.amplitudeValue = this.value;
    }

    var freqSlider = document.getElementById("myFrequencyRange");
    if (!window.hasOwnProperty('frequencyValue'))
    {
        window.frequencyValue = 50;
    }
    freqSlider.value = window.frequencyValue;
    var freqOutput = document.getElementById("frequencyDemo");
    freqOutput.innerHTML = freqSlider.value + " Hz";

    freqSlider.oninput = function()
    {
        freqOutput.innerHTML = this.value + " Hz";
        window.frequencyValue = this.value;
    }
    
    var channelSlider = document.getElementById("myChannelRange");
    if (!window.hasOwnProperty('channelValue'))
    {
        window.channelValue = 0;
    }
    channelSlider.value = window.channelValue;
    var channelOutput = document.getElementById("channelDemo");
    channelOutput.innerHTML = channelSlider.value;

    channelSlider.oninput = function()
    {
        channelOutput.innerHTML = this.value;
        window.channelValue = this.value;
    }
    
    var profileSlider = document.getElementById("myProfileRange");
    if (!window.hasOwnProperty('profileValue'))
    {
        window.profileValue = 0;
    }
    profileSlider.value = window.profileValue;
    var profileOutput = document.getElementById("profileDemo");
    profileOutput.innerHTML = profileSlider.value;

    profileSlider.oninput = function()
    {
        profileOutput.innerHTML = this.value;
        window.profileValue = this.value;
    }
    
    var phaseSlider = document.getElementById("myPhaseRange");
    if (!window.hasOwnProperty('phaseValue'))
    {
        window.phaseValue = 0;
    }
    phaseSlider.value = window.phaseValue;
    var phaseOutput = document.getElementById("phaseDemo");
    phaseOutput.innerHTML = phaseSlider.value + "&deg";

    phaseSlider.oninput = function()
    {
        phaseOutput.innerHTML = this.value + "&deg";
        window.phaseValue = this.value;
    }
}

function SetElements()
{
    for (element in possibleHTMLelements)
    {
        let HTMLElement = document.getElementById(element + "checkbox");
        if (HTMLElement !== null)
        {
            possibleHTMLelements[element]["status"] = HTMLElement.checked;
        }
    }
    UpdateElementsOnPage();
    SendBack(JSON.stringify({"function": "gui_change", "instructions": ["update_gui", possibleHTMLelements]}));
}

function ListHTMLElements()
{
    HTMLElementsList = document.getElementById("ListHTMLElements");
    if (HTMLElementsList.getAttribute("expanded") === "false")
    {
        HTMLElementsList.innerHTML += "<br/>";
        for (element in possibleHTMLelements)
        {
            var tempString =
            String.raw
            `
            <div class="row">
                <div class="col-sm" align = "left">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
                        <label class="form-check-label" for="flexCheckDefault">
                            Default checkbox
                        </label>
                    </div>
                </div>
            </div>
            `
            tempString = tempString.replace("flexCheckDefault", element+"checkbox"); //1st instance
            tempString = tempString.replace("flexCheckDefault", element+"checkbox"); //2nd instance
            tempString = tempString.replace("Default checkbox", element);
            if (!possibleHTMLelements[element]["status"])
            {
                tempString = tempString.replace("checked", "");
            }
            HTMLElementsList.innerHTML += tempString + "\n";
        }
        HTMLElementsList.setAttribute("expanded", "true");
        HTMLElementsList.innerHTML += "\n" +
        String.raw
        `
            <br/>
            <button type="button" class="btn btn-success" onclick="SetElements()">Submit</button>
        `;
    }
    else
    {
        HTMLElementsList.innerHTML =
        String.raw
        `
            <div class="row">
                <div class="col-sm" align = "right" id = "ListHTMLElementsButton" onclick = "ListHTMLElements()" onmouseover="this.style.cursor='pointer'" onmouseleave="this.style.cursor='default'">
                        &#43;
                </div>
                <div class="col-sm-11" align = "left">
                    Add or Remove HTML Elements
                </div>
            </div>
        `;
        HTMLElementsList.setAttribute("expanded", "false");
    }
}

function StoreCoordinates(element = "all")
{
    if (element == "all")
    {
        for (elem in possibleHTMLelements)
        {
            let tempElem = document.getElementById(elem);
            if (tempElem !== null)
            {
                let rect = tempElem.getBoundingClientRect();
                let left = tempElem.style.left || rect.left + "px";
                let top = tempElem.style.top || rect.top + "px";
//                console.log(rect.left, rect.top, left, top);
                possibleHTMLelements[elem]["coordinates"] = [left, top];
                console.log(elem, possibleHTMLelements[elem]["coordinates"]);
            }
        }
        SendBack(JSON.stringify({"function": "gui_change", "instructions": ["update_gui", possibleHTMLelements]}));
        return;
    }
    let tempElem = document.getElementById(element);
    if (tempElem !== null)
    {
        let rect = tempElem.getBoundingClientRect();
        let left = tempElem.style.left || rect.left + "px";
        let top = tempElem.style.top || rect.top + "px";
        possibleHTMLelements[elem]["coordinates"] = [left, top];
    }
    SendBack(JSON.stringify({"function": "gui_change", "instructions": ["update_gui", possibleHTMLelements]}));
}

function UpdateElementsOnPage(save = true)
{
    for (elem in possibleHTMLelements)
    {
        let element = document.getElementById(elem);
        if (!possibleHTMLelements[elem]["status"] && element) //if the user doesn't want this element but it's still on the html
        {
            document.getElementById(elem).parentNode.removeChild(element); //remove element
        }
        else if (possibleHTMLelements[elem]["status"] && !element) //if the user wants this element but it's not on the html
        {
            var temp = document.createElement('row'); //create a row element
            temp.innerHTML = possibleHTMLelements[elem]["html"];
            temp.innerHTML = temp.innerHTML.replace("gui_elements", gui_elements); //you'll have to do this for all elements with django variables inside
            // Search for an element within temp by id
            let tempElem = "#"+elem;
            // All possibleHTMLelements are draggable
            temp.querySelector(tempElem).addEventListener('dragstart', startDrag, true);
            temp.querySelector(tempElem).addEventListener('dragend', endDrag, true);
            
            document.getElementById("whole_html").appendChild(temp);
        }
    }
    
    if (save)
    {
        StoreCoordinates();
    }
}

function ResetElements()
{
    Object.keys(possibleHTMLelements).forEach(key => {
        possibleHTMLelements[key].status = true; // set the "status" value to true for each key
    });
    for (element in possibleHTMLelements)
    {
        let HTMLElement = document.getElementById(element + "checkbox");
        if (HTMLElement !== null)
        {
            HTMLElement.checked = possibleHTMLelements[element]["status"];
        }
    }
    
    document.getElementById("whole_html").innerHTML =
    String.raw
    `
    <br/><br/>
    <div class="row">
        <div class="col-sm offset-sm-6" id="add-experiment-search-bar" align="center" draggable="true">
                            <div class="input-group" align = "center">
    <!--                            mr-5 means 0.25 rem * 5 = 1.25rem, equal to 5 spaces-->
                                <input type="text" class="form-control mr-5" id="SearchForExperimentInput" placeholder="Experiment Name" style="display: inline-block;" onkeydown="if(event.keyCode === 13) { SearchForExperiment(); }">
                                <button class="btn btn-info" type="button" onclick = "SearchForExperiment()">Search For Experiment  &nbsp; &#128269; &#128170; &#128300; &#129515; &#129514;</button>
                            </div>
                            
        </div>
    </div>
    <!--⌄⌄⌄ heat-map and line graph ⌄⌄⌄-->
    <div class="row">
        <div class="col-sm" id="heat-map-line-graph-show" align = "center" draggable="true">
        </div>
    </div>
    <br/>
    <br/>
    <div class="row">
        <div class="col-sm" id="voltages" align = "center" draggable="true">
        </div>
    </div>
    <br/>
    <div class="row">
        <div class="col-sm" align = "center" draggable = "true" id = "time_diff" draggable = "true">
            <label for="timediff" class = "foo">&nbsp Time Difference for Camera Data (seconds):&nbsp</label>
            <input type = "text" id="timediff" name = "timediff" readonly>
        </div>
    </div>
    <br/>
    <br/>

    <!--Buttons on document to Start data streaming (Start()), Stop data streaming (Stop()), and send a signal back to the subscriber in server.py (SendBack()) respectively ⌄⌄⌄-->
    <div class = "row">
        <div class="col-sm" align = "center" draggable = "true" id = "Start">
            <button type="button" class="btn btn-success" onclick="Start(); ResumeAnimations();">Start!</button>
        </div>
        <div class="col-sm" align = "center" draggable = "true" id = "Stop">
            <button type="button" class="btn btn-danger" onclick="Stop(); PauseAnimations();">Stop!</button>
        </div>
        <div class="col-sm" align = "center" draggable = "true" id = "Signal">
            <button type="button" class="btn btn-warning" onclick="SendBack('{&quot;function&quot;: &quot;signal&quot;, &quot;instructions&quot;: &quot;Hi friend!!&quot;}')">Signal!</button>
        </div>
    </div>
    
    <br/><br/>

    
    <div class = "row">
        <div class="col-sm" align = "center" id="dropdownMenuButtonSetFreqAmplChanPhaseOutput" draggable = "true">
            <button type="button" class="btn btn-info" onclick="FreqAmplChanPhaseSetter();">
                Set Output
            </button>
        </div>
        
        <div class="col-sm" align = "center" id="dropdownMenuButtonChanOutput" draggable = "true">
            <button type="button" class="btn btn-info" onclick="ChannelSetter();">
                Read Temperature
            </button>
        </div>
    </div>
    
    <br/><br/><br/>
    <br/><br/><br/>
    
    <div class="row">
        <!--load user's gui elements at the end of the document in the django variable 'gui_elements' -->
        <div class="col-sm" id = "users_html">
            gui_elements
        </div>
    </div>
    `.replaceAll("gui_elements", gui_elements);
    
    UpdateElementsOnPage();
    AddDragEventListeners();
}

function SetElementsToLastSavedCoordinates()
{
    for (element in possibleHTMLelements)
    {
        let elem = document.getElementById(element);
        if (elem !== null && possibleHTMLelements[element]["coordinates"] !== undefined)
        {
            Coordinates = possibleHTMLelements[element]["coordinates"];
            X = Coordinates[0];
            Y = Coordinates[1];
            console.log(element, X, Y);
            elem.style.left = X;
            elem.style.top = Y;
        }
    }
}

//Adds dragging event listeners for all elements
//------------------------------------------------
function AddDragEventListeners()
{
    const collection = document.getElementsByClassName("outer_square");
    for (let i = 0; i < collection.length; i++)
    {
        collection[i].addEventListener('dragstart', startDrag, true);
        collection[i].addEventListener('dragend', endDrag, true);
    }

    const add_experiment_search_bar_elem = document.getElementById("add-experiment-search-bar");
    if (add_experiment_search_bar_elem !== null)
    {
        add_experiment_search_bar_elem.addEventListener('dragstart', startDrag, true);
        add_experiment_search_bar_elem.addEventListener('dragend', endDrag, true);
    }
    
    const heat_map_line_graph_elem = document.getElementById("heat-map-line-graph-show");
    if (heat_map_line_graph_elem !== null)
    {
        heat_map_line_graph_elem.addEventListener('dragstart', startDrag, true);
        heat_map_line_graph_elem.addEventListener('dragend', endDrag, true);
    }

    const voltages_elem = document.getElementById("voltages");
    if (voltages_elem !== null)
    {
        voltages_elem.addEventListener('dragstart', startDrag, true);
        voltages_elem.addEventListener('dragend', endDrag, true);
    }

    const time_diff_elem = document.getElementById("time_diff");
    if (time_diff_elem !== null)
    {
        time_diff_elem.addEventListener('dragstart', startDrag, true);
        time_diff_elem.addEventListener('dragend', endDrag, true);
    }

    const Start_elem = document.getElementById("Start");
    if (Start_elem !== null)
    {
        Start_elem.addEventListener('dragstart', startDrag, true);
        Start_elem.addEventListener('dragend', endDrag, true);
    }

    const Stop_elem = document.getElementById("Stop");
    if (Stop_elem !== null)
    {
        Stop_elem.addEventListener('dragstart', startDrag, true);
        Stop_elem.addEventListener('dragend', endDrag, true);
    }

    const Signal_elem = document.getElementById("Signal");
    if (Signal_elem !== null)
    {
        Signal_elem.addEventListener('dragstart', startDrag, true);
        Signal_elem.addEventListener('dragend', endDrag, true);
    }

    const dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem = document.getElementById("dropdownMenuButtonSetFreqAmplChanPhaseOutput");
    if (dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem !== null)
    {
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.addEventListener('dragstart', startDrag, true);
        dropdownMenuButtonSetFreqAmplChanPhaseOutput_elem.addEventListener('dragend', endDrag, true);
    }

    const dropdownMenuButtonChanOutput_elem = document.getElementById("dropdownMenuButtonChanOutput");
    if (dropdownMenuButtonChanOutput_elem !== null)
    {
        dropdownMenuButtonChanOutput_elem.addEventListener('dragstart', startDrag, true);
        dropdownMenuButtonChanOutput_elem.addEventListener('dragend', endDrag, true);
    }
}

//                *******************
//                *      "Main"     *
//                *******************

console.log(username); //logging the user's username to console
console.log("connected!");
window.chatSocket = new WebSocket(     //creating new WebSocket instance
            'ws://'
            + window.location.host
           + '/ws/members/'
        );

AddDragEventListeners();
Start(); //start data streaming
