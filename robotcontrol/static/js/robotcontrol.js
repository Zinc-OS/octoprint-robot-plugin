/*
 * View model for robotcontrol
 *
 * Author: Louis Sarwal
 * License: AGPLv3
 */

$(function() {
	function RobotControlViewModel(parameters) {
		var self = this;
		self.params = parameters;
		self.printerState = parameters[0];
		self.loginState = parameters[1];
		self.files = parameters[2];
		self.settings = parameters[3];
        self.onBeforeBinding = function() {
            self.load();
            self.time=self.getTime()
        }
        var x=false
        //to make sure not too many ajax requests are being sent
        self.getTime = function(){
            var date = new Date();
            var time = date.getTime();
            return time;
        }
       self.load = function() {
           
            $('#boxes').html("");
						$('#boxes').html("");
						for(var i = 1; i <=4; i++) {
							var row;
                            row = $('<div class="control-group" <label class="control-label">Servo '+i+'</label> <div class="controls"><input data-number = "'+i+'" type="range" class="texto input-block-level" value="15" min="1" max="29"></div></div>');
                            row.find(".texto").on("input",function() {
                                    var arm= parseInt(this.value);
                                    self.servo($(this).data("number"),arm);                              
                            });
                            row.find(".texto").mouseup(function() {
                                    var arm= parseInt(this.value);
                                    self.add_gcode($(this).data("number"),arm*6);                              
                            });
                            
                           
                             $('#boxes').append(row);
                        }
                }
                
        self.add_gcode = function(servo, angle) {		
            var row = $('<div>servo'+servo+':'+angle+'</div>');
            $('#gcode-gen').append(row);
                        
        }
                
        self.servo=function(servo,angle){
            //if (self.getTime()-self.time>200){
                $.ajax({
                        url: "plugin/robotcontrol/servo"+ servo +"?angle="+angle*6,
                        type: "GET",
                        dataType: "text",
                        headers: {"X-Api-Key":UI_API_KEY},
                        success: function(c) {
                             $("#success").text(c);
                        },
                        error: function() {

                        }
                    
            

         });
                self.time=self.getTime()
           // }
         /*
           / OctoPrint.get( "plugin/continuousprint/servo"+servo+"?angle="+angle,)
            .done(function(response) {
               $("#success").html(response);
            })
            */
            
        }
    }
		

	// This is how our plugin registers itself with the application, by adding some configuration
	// information to the global variable OCTOPRINT_VIEWMODELS
	OCTOPRINT_VIEWMODELS.push([
		// This is the constructor to call for instantiating the plugin
		RobotControlViewModel,

		// This is a list of dependencies to inject into the plugin, the order which you request
		// here is the order in which the dependencies will be injected into your view model upon
		// instantiation via the parameters argument
		["printerStateViewModel", "loginStateViewModel", "filesViewModel", "settingsViewModel"],

		// Finally, this is the list of selectors for all elements we want this view model to be bound to.
		["#tab_plugin_robotcontrol"]
	]);
});
