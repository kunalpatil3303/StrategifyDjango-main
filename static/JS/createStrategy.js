
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();

var prevDate = document.getElementById("startDate");
var todayDate = document.getElementById('stopDate');
prevDate.defaultValue  = parseInt(yyyy)-5+"-"+mm+"-"+dd;
todayDate.defaultValue  = yyyy+"-"+mm+"-"+dd;

let indicatorsuggestions = [["MA","Moving Average"],["EMA","Exponential Moving Average"],["WMA","Weighted Moving Average"],["RSI","Relative Strength Index"],["Value","Value"],["Close","Close"]];

var indicatorWrapper = document.querySelector(".indicator-search");
var indicatorInputBox = indicatorWrapper.querySelector("input");
var indicatorSuggBox, indicatorSuggBox2, indicatorSuggBox3, indicatorSuggBox4;

function lookup(arg){
    var id = arg.getAttribute('id');
    var no = id.charAt(id.length-1);
    var value = arg.value;
    let userData = value;
    let emptyArray = [];
    let dataArray = [];
    var string = "#firindicatorBox"+no.toString();
    indicatorSuggBox = indicatorWrapper.querySelector(string);
    if(userData){
        emptyArray = indicatorsuggestions.filter((data)=>{
            return data[0].toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        dataArray = emptyArray;
        emptyArray = emptyArray.map((data)=>{
            return data = `<li></li>`;
        });
        indicatorSuggBox.classList.add("active");
        showIndicatorSuggestions(emptyArray);
        let allList = indicatorSuggBox.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            let head = document.createElement("p");
            let desc = document.createElement("p");
            head.innerHTML = dataArray[i][0];
            desc.innerHTML = dataArray[i][1]
            head.classList.add("indicatorsuggestionHead");
            desc.classList.add("indicatorsuggestionDesc");
            allList[i].appendChild(head);
            allList[i].appendChild(desc);
            allList[i].setAttribute("name", 'this.innerText');
            allList[i].setAttribute("onclick", "openIndicatorDetails('"+dataArray[i][0]+"',"+no+")");
        }
    }else{
        indicatorSuggBox.classList.remove("active");
        dataArray = [];
    }
}


function showIndicatorSuggestions(list){
    let listData;
    if(!list.length){
        userValue = indicatorInputBox.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    indicatorSuggBox.innerHTML = listData;
}

function openIndicatorDetails(element,id){
    if(element == "Close"){
        $('#indicatorCloseModal').modal();
        let x = document.getElementById('indicatorheadingModal');
        x.innerHTML = element;
        let y = document.getElementById('closemodalIndicator');
        y.setAttribute("onclick","saveIndicatordetails("+id+");")
    }else{
        $('#indicatorModal').modal();
        let x = document.getElementById('indicatorheadingModal');
        x.innerHTML = element;
        let y = document.getElementById('modalIndicator');
        y.setAttribute("onclick","saveIndicatordetails("+id+");")
    }
    
}

function saveIndicatordetails(id){
    var z = document.getElementById('indicatorheadingModal').innerHTML;
    if(z == "Close"){
        var x = 0;
        document.getElementsByName("entryfirindicator"+id.toString())[0].value = z+","+x;
        document.getElementById('firindicatorBox'+id.toString()).innerHTML = "";    
        indicatorSuggBox.classList.remove("active");
        $('#indicatorCloseModal').modal('hide');
    }else{
        var x = document.getElementsByName("period1")[0].value;
        var y = document.getElementsByName("period2")[0].value;
        document.getElementsByName("entryfirindicator"+id.toString())[0].value = z+","+x;
        document.getElementsByName("entrysecindicator"+id.toString())[0].value = z+","+y;
        document.getElementById('firindicatorBox'+id.toString()).innerHTML = "";    
        indicatorSuggBox.classList.remove("active");
        $('#indicatorModal').modal('hide');
    }
    

}

function lookup2(arg){

    var id = arg.getAttribute('id');
    var no = id.charAt(id.length-1);
    var value = arg.value;
    let userData = value;
    let emptyArray = [];
    let dataArray = [];
    var string = "#secindicatorBox"+no.toString();
    indicatorSuggBox2 = indicatorWrapper.querySelector(string);
    if(userData){
        emptyArray = indicatorsuggestions.filter((data)=>{
            return data[0].toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        dataArray = emptyArray;
        emptyArray = emptyArray.map((data)=>{
            return data = `<li></li>`;
        });
        indicatorSuggBox2.classList.add("active");
        showIndicatorSuggestions2(emptyArray);
        let allList = indicatorSuggBox2.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            let head = document.createElement("p");
            let desc = document.createElement("p");
            head.innerHTML = dataArray[i][0];
            desc.innerHTML = dataArray[i][1]
            head.classList.add("indicator2suggestionHead");
            desc.classList.add("indicator2suggestionDesc");
            allList[i].appendChild(head);
            allList[i].appendChild(desc);
            allList[i].setAttribute("name", 'this.innerText');
            allList[i].setAttribute("onclick", "openIndicator2Details('"+dataArray[i][0]+"',"+no+")");
        }
    }else{
        indicatorSuggBox2.classList.remove("active");
        dataArray = [];
    }
}

function showIndicatorSuggestions2(list){
    let listData;
    if(!list.length){
        userValue = indicatorInputBox.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    indicatorSuggBox2.innerHTML = listData;
}

function openIndicator2Details(element,id){
    if(element == "Close"){
        $('#indicatorCloseModal').modal('show')
        let y = document.getElementById('closemodalIndicator');
        y.setAttribute("onclick","saveIndicatordetails2("+id+");");
        let x = document.getElementById('indicator2headingModal');
        x.innerHTML = element;
    }else{
        $('#indicator2Modal').modal('show')
        let y = document.getElementById('modalIndicator2');
        y.setAttribute("onclick","saveIndicatordetails2("+id+");");
        let x = document.getElementById('indicator2headingModal');
        x.innerHTML = element;
    }
    
}


function saveIndicatordetails2(id){
    var y = document.getElementsByName("indicatorperiod22")[0].value;
    var z = document.getElementById('indicator2headingModal').innerHTML
    if(z == "Close"){
        y = 0;
        document.getElementsByName("entrysecindicator"+id.toString())[0].value = z+","+y;
        indicatorSuggBox2.classList.remove("active");
        $('#indicatorCloseModal').modal('hide');
    }
    document.getElementsByName("entrysecindicator"+id.toString())[0].value = z+","+y;
    indicatorSuggBox2.classList.remove("active");
    $('#indicator2Modal').modal('hide');
}




var indicatorWrapper2;
var indicatorInputBox2;


function lookup3(arg){
    indicatorWrapper2 = document.querySelector(".indicator-search3");
    indicatorInputBox2 = indicatorWrapper2.querySelector("input");

    var id = arg.getAttribute('id');
    var no = id.charAt(id.length-1);
    var value = arg.value;
    let userData = value;
    let emptyArray = [];
    let dataArray = [];
    var string = "#exitfirindicatorBox"+no.toString();
    indicatorSuggBox3 = indicatorWrapper2.querySelector(string);
    if(userData){
        emptyArray = indicatorsuggestions.filter((data)=>{
            return data[0].toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        dataArray = emptyArray;
        emptyArray = emptyArray.map((data)=>{
            return data = `<li></li>`;
        });
        indicatorSuggBox3.classList.add("active");
        showIndicatorSuggestions3(emptyArray);
        let allList = indicatorSuggBox3.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            let head = document.createElement("p");
            let desc = document.createElement("p");
            head.innerHTML = dataArray[i][0];
            desc.innerHTML = dataArray[i][1]
            head.classList.add("indicatorsuggestionHead");
            desc.classList.add("indicatorsuggestionDesc");
            allList[i].appendChild(head);
            allList[i].appendChild(desc);
            allList[i].setAttribute("name", 'this.innerText');
            allList[i].setAttribute("onclick", "openIndicator3Details('"+dataArray[i][0]+"',"+no+")");
        }
    }else{
        indicatorSuggBox3.classList.remove("active");
        dataArray = [];
    }
}

function showIndicatorSuggestions3(list){
    let listData;
    if(!list.length){
        userValue = indicatorInputBox.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    indicatorSuggBox3.innerHTML = listData;
}


function openIndicator3Details(element,id){
    if(element == "Close"){
        $('#indicatorCloseModal').modal();
        let x = document.getElementById('indicatorheadingModal');
        x.innerHTML = element;
        let y = document.getElementById('closemodalIndicator');
        y.setAttribute("onclick","saveIndicatordetails3("+id+");")
    }else{
        $('#indicatorModal').modal();
        let x = document.getElementById('indicatorheadingModal');
        x.innerHTML = element;
        let y = document.getElementById('modalIndicator');
        y.setAttribute("onclick","saveIndicatordetails3("+id+");")
    }
    
}

function saveIndicatordetails3(id){
    var z = document.getElementById('indicatorheadingModal').innerHTML;
    if(z == "Close"){
        var x = "0";
        document.getElementsByName("exitfirindicator"+id.toString())[0].value = z+","+x;
        indicatorSuggBox3.classList.remove("active");
        $('#indicatorCloseModal').modal('hide');
    }else{
        var x = document.getElementsByName("period1")[0].value;
        var y = document.getElementsByName("period2")[0].value;
        document.getElementsByName("exitfirindicator"+id.toString())[0].value = z+","+x;
        document.getElementsByName("exitsecindicator"+id.toString())[0].value = z+","+y;
        indicatorSuggBox3.classList.remove("active");
        $('#indicatorModal').modal('hide');
    }
    
}

function lookup4(arg){

    indicatorWrapper2 = document.querySelector(".indicator-search3");
    indicatorInputBox2 = indicatorWrapper2.querySelector("input");


    var id = arg.getAttribute('id');
    var no = id.charAt(id.length-1);
    var value = arg.value;
    let userData = value;
    let emptyArray = [];
    let dataArray = [];
    var string = "#exitsecindicatorBox"+no.toString();
    indicatorSuggBox4 = indicatorWrapper2.querySelector(string);
    if(userData){
        emptyArray = indicatorsuggestions.filter((data)=>{
            return data[0].toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        dataArray = emptyArray;
        emptyArray = emptyArray.map((data)=>{
            return data = `<li></li>`;
        });
        indicatorSuggBox4.classList.add("active");
        showIndicatorSuggestions4(emptyArray);
        let allList = indicatorSuggBox4.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            let head = document.createElement("p");
            let desc = document.createElement("p");
            head.innerHTML = dataArray[i][0];
            desc.innerHTML = dataArray[i][1]
            head.classList.add("indicatorsuggestionHead");
            desc.classList.add("indicatorsuggestionDesc");
            allList[i].appendChild(head);
            allList[i].appendChild(desc);
            allList[i].setAttribute("name", 'this.innerText');
            allList[i].setAttribute("onclick", "openIndicator4Details('"+dataArray[i][0]+"',"+no+")");
        }
    }else{
        indicatorSuggBox4.classList.remove("active");
        dataArray = [];
    }
}

function showIndicatorSuggestions4(list){
    let listData;
    if(!list.length){
        userValue = indicatorInputBox.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    indicatorSuggBox4.innerHTML = listData;
}

function openIndicator4Details(element,id){
    if(element == "Close"){
        $('#indicatorCloseModal').modal('show');
        let x = document.getElementById('indicator2headingModal');
        x.innerHTML = element;
        let y = document.getElementById('closemodalIndicator');
        y.setAttribute("onclick","saveIndicatordetails4("+id+");");
    }else{
        $('#indicator2Modal').modal('show')
        let x = document.getElementById('indicator2headingModal');
        x.innerHTML = element;
        let y = document.getElementById('modalIndicator2');
        y.setAttribute("onclick","saveIndicatordetails4("+id+");");
    }
}

function saveIndicatordetails4(id){

    var y = document.getElementsByName("indicatorperiod22")[0].value;
    var z = document.getElementById('indicator2headingModal').innerHTML

    if(z == "Close"){
        var x = "0";
        document.getElementsByName("exitsecindicator"+id.toString())[0].value = z+","+x;
        indicatorSuggBox4.classList.remove("active");
        $('#indicatorCloseModal').modal('hide');
    }else{
        document.getElementsByName("exitsecindicator"+id.toString())[0].value = z+","+y;
        indicatorSuggBox4.classList.remove("active");
        $('#indicator2Modal').modal('hide');
    }
}
