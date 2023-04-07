

function openNav() {
  document.getElementById("mySidenav").style.display = "inline-block";
}

function closeNav() {
  document.getElementById("mySidenav").style.display = "none";
}


var entryCounter = 2;
function addEntryRow(){
    var div = document.createElement('div');
    div.className = 'row fadeIn';
    div.id = 'inputEntryFormRow';
    div.innerHTML =  
                    `<div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12">`+
                        `<div class="indicator-search">`+
                            `<input type="text" name="entryfirindicator`+entryCounter+`" placeholder="Indicator" class="form-control" autocomplete="off" id="entryfirindicator`+entryCounter+`" onkeyup="lookup(this);" required>`+
                            `<ul class="indicatorsuggest-box" id="firindicatorBox`+entryCounter+`"></ul>`+
                        `</div>`+
                    `</div>`+
                    `<div class="col-lg-3 col-xl-3 col-md-12 col-sm-12 col-xs-12">`+
                        `<select class="form-select form-control" id="entrycomparator`+entryCounter+`" name="entrycomparator`+entryCounter+`" aria-label="Default select example">`+
                                                `<option value="0">Crosses Below</option><option value="1">Equal To</option><option selected value="2">Crosses Above</option></select>`+
                    `</div>`+
                    `<div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12">`+
                        `<input type="text" name="entrysecindicator`+entryCounter+`" id="entrysecindicator`+entryCounter+`" placeholder="Indicator" class="form-control" onkeyup="lookup2(this)" required >`+
                        `<ul class="indicatorsuggest-box2" id="secindicatorBox`+entryCounter+`"></ul></div><div class="col-1">`+
                        `<span class="w-50 h-50 deleteEntryRow" onclick="removeEntryRow(this)" style="font-size:3rem">&times;</span>`+
                    `</div>`
                            
    document.getElementById('entryConditionRow').appendChild(div);
    entryCounter += 1;
}

function removeEntryRow(input) {
    console.log(input)
    input.parentNode.parentNode.remove()
}


var exitCounter = 1;
function addExitRow(){
    var div = document.createElement('div');
    div.className = 'row fadeIn';
    div.id = 'inputExitFormRow';
    div.innerHTML = 
                    `<div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12">`+
                            `<input type="text" name="exitfirindicator`+exitCounter+`" placeholder="Indicator" class="form-control" autocomplete="off" id="exitfirindicator`+exitCounter+`" onkeyup="lookup3(this);" required>`+
                            `<ul class="indicatorsuggest-box3" id="exitfirindicatorBox`+exitCounter+`"></ul>`+
                    `</div>`+
                    `<div class="col-lg-3 col-xl-3 col-md-12 col-sm-12 col-xs-12">`+
                        `<select class="form-select form-control" id="exitcomparator`+exitCounter+`" name="exitcomparator`+exitCounter+`" aria-label="Default select example">`+
                                                `<option selected value="0">Crosses Below</option><option value="1">Equal To</option><option selected value="2">Crosses Above</option></select>`+
                    `</div>`+
                    `<div class="col-lg-4 col-xl-4 col-md-12 col-sm-12 col-xs-12">`+
                        `<input type="text" name="exitsecindicator`+exitCounter+`" id="exitsecindicator`+exitCounter+`" placeholder="Indicator" class="form-control" onkeyup="lookup4(this)" required>`+
                        `<ul class="indicatorsuggest-box4" id="exitsecindicatorBox`+exitCounter+`"></ul></div><div class="col-1">`+
                        `<span class="w-50 h-50 deleteExitRow" onclick="removeExitRow(this)" style="font-size:3rem">&times;</span>`+
                    `</div>`

    document.getElementById('exitConditionRow').appendChild(div);
    exitCounter += 1;
}

function removeExitRow(input) {
    input.parentNode.parentNode.remove()
}






