# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
import flask, json
from octoprint.server.util.flask import restricted_access
from octoprint.events import eventManager, Events
import smbus2
import time
import sys
import os
# I no longer understand my own code 
class RobotControlPlugin(octoprint.plugin.SettingsPlugin,
							octoprint.plugin.TemplatePlugin,
							octoprint.plugin.AssetPlugin,
							octoprint.plugin.StartupPlugin,
							octoprint.plugin.BlueprintPlugin,
							octoprint.plugin.EventHandlerPlugin,
							octoprint.plugin.SimpleApiPlugin,
							octoprint.plugin.OctoPrintPlugin):
	
	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			servo1Min="0",
			servo2Min="0",
			servo3Min="0",
			servo4Min="0",
			servo1Max="180",
			servo2Max="180",
			servo3Max="180",
			servo4Max="180",
			addr="3",
			available="[]"
			
			
		)

	##~~ StartupPlugin mixin
	def on_after_startup(self):
		self._logger.info("Robot Control Plugin started")
		self._settings.save()
		self.getAddresses()
		self.time=time.time()
		
	def getAddresses(self):
		availableArray=[]
		n=1
		while n<128:
			if n<0x10:
				available=os.popen('i2cdetect -y 1 | grep 0'+hex(n))
			else:
				available=os.popen('i2cdetect -y 1 | grep '+hex(n))
			if available != "":
				availableArray.append(n)
			n+=1
		self._settings.set(["available"],json.dumps(availableArray))
		self._settings.save()
		
		
			
		
			
		


#
			#try:
			##	self.setAngle1(servo,address)
			#except OSError:
			#	e = sys.exc_info()[0]
			#	self._logger.error("%s", e)
			#	return flask.make_response("error", 200)
				
	def gcode_set_angle(self,comm,line, *args, **kwargs):
		if line.startswith("servo"):
			self._logger.info("gcode recieved")
			self.time=time.time()
			addr = int(self._settings.get(["addr"]))
			angle = int(line.split(":")[1])
			servo = int(line.split("o")[1].split(":")[0])
			#angle is an integer from 0 to 180
			if angle<int(self._settings.get(["servo1Max"])) and angle>int(self._settings.get(["servo1Min"])):
				realAngle=angle/6
				if servo == 1:
					n=int(realAngle)
				elif servo == 2:
					n=int(realAngle)+32
				elif servo == 3:
					n=int(realAngle)+64
				elif servo == 4:
					n=int(realAngle)+96
				else:
					self._logger.error("%s", "SERVO DOES NOT EXIST")
				try:
					smbus2.SMBus(1).i2c_rdwr(smbus2.i2c_msg.write(addr, [n]))
				except:
					e = sys.exc_info()[0]
					self._logger.error("%s", e)

			#time.sleep(1)
				
            			
	@octoprint.plugin.BlueprintPlugin.route("/servo1", methods=["GET"])
	@restricted_access
	def setAngle1(self):
		if time.time()-self.time>0.1:#Make sure time between i2c attempts is not too small TODO: set as setting
			self.time=time.time()
			addr = int(self._settings.get(["addr"]))
			angle = int(flask.request.args.get("angle", 0))
			#angle is an integer from 0 to 180
			if angle<int(self._settings.get(["servo1Max"])) and angle>int(self._settings.get(["servo1Min"])):
				realAngle=angle/6
				n=int(realAngle)
				try:
					smbus2.SMBus(1).i2c_rdwr(smbus2.i2c_msg.write(addr, [n]))
				except:
					e = sys.exc_info()[0]
					self._logger.error("%s", e)
					return flask.make_response("error", 200)
				#time.sleep(1)
				return flask.make_response("success", 200)
		return flask.make_response("Too Fast!", 200)
	@octoprint.plugin.BlueprintPlugin.route("/servo2", methods=["GET"])
	@restricted_access			
	def setAngle2(self):
		if time.time()-self.time>0.1:#Make sure time between i2c attempts is not too small TODO: set as setting
			self.time=time.time()
			addr = int(self._settings.get(["addr"]))
			angle = int(flask.request.args.get("angle", 0))
			if angle<int(self._settings.get(["servo2Max"])) and angle>int(self._settings.get(["servo2Min"])):
				#angle is an integer from 0 to 180
				realAngle=angle/6
				n=32+int(realAngle)
				try:
					smbus2.SMBus(1).i2c_rdwr(smbus2.i2c_msg.write(addr, [n]))
				except:
					e = sys.exc_info()[0]
					self._logger.error("%s", e)
					return flask.make_response("error", 200)
				#time.sleep(1)
				return flask.make_response("success", 200)
		return flask.make_response("Too Fast!", 200)
	@octoprint.plugin.BlueprintPlugin.route("/servo3", methods=["GET"])
	@restricted_access
	def setAngle3(self):
		if time.time()-self.time>0.1:#Make sure time between i2c attempts is not too small TODO: set as setting
			self.time=time.time()
			addr = int(self._settings.get(["addr"]))
			angle = int(flask.request.args.get("angle", 0))
			if angle<int(self._settings.get(["servo3Max"])) and angle>int(self._settings.get(["servo3Min"])):
				
				#angle is an integer from 0 to 180
				realAngle=angle/6
				n=64+int(realAngle)
				try:
					smbus2.SMBus(1).i2c_rdwr(smbus2.i2c_msg.write(addr, [n]))
				except:
					e = sys.exc_info()[0]
					self._logger.error("%s", e)
					return flask.make_response("error", 200)
				#time.sleep(1)
				return flask.make_response("success", 200)
		return flask.make_response("Too Fast!", 200)
	@octoprint.plugin.BlueprintPlugin.route("/servo4", methods=["GET"])
	@restricted_access		
	def setAngle4(self):
		if time.time()-self.time>0.1:#Make sure time between i2c attempts is not too small TODO: set as setting
			self.time=time.time()
			addr = int(self._settings.get(["addr"]))
			angle = int(flask.request.args.get("angle", 0))
			if angle<int(self._settings.get(["servo4Max"])) and angle>int(self._settings.get(["servo4Min"])):
				
				#angle is an integer from 0 to 180
				realAngle=angle/6
				n=96+int(realAngle)
				try:
					smbus2.SMBus(1).i2c_rdwr(smbus2.i2c_msg.write(addr, [n]))
				except:
					e = sys.exc_info()[0]
					self._logger.error("%s", e)
					return flask.make_response("error", 200)
				#time.sleep(1)
				return flask.make_response("success", 200)
		return flask.make_response("Too Fast!", 200)
			
	
	@octoprint.plugin.BlueprintPlugin.route("/up4", methods=["GET"])
	@restricted_access
	def setAddress(self):
		address = int(flask.request.args.get("address", 0))
		addresses = json.loads(self._settings.get(["available"]))
		if address in addresses:
			self._settings.set(["addr"],address)
			self._settings.save()		
		
		

	##~~  TemplatePlugin
	def get_template_vars(self):
		return dict(
			servo1Min=self._settings.get(["servo1Min"]),
			servo2Min=self._settings.get(["servo2Min"]),
			servo3Min=self._settings.get(["servo3Min"]),
			servo4Min=self._settings.get(["servo4Min"]),
			servo1Max=self._settings.get(["servo1Max"]),
			servo2Max=self._settings.get(["servo2Max"]),
			servo3Max=self._settings.get(["servo3Max"]),
			servo4Max=self._settings.get(["servo4Max"]),
			addr="3",
			available="[]"
			
			
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False, template="robotcontrol_settings.jinja2"),
			dict(type="tab", custom_bindings=False, template="robotcontrol_tab.jinja2")
		]
	##~~ AssetPlugin
	def get_assets(self):
		return dict(
			js=["js/robotcontrol.js"]
		)
	##~~ Softwareupdate hook
	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			robotcontrol=dict(
				displayName="Robot Control Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Zinc-OS",
				repo="octoprint-robot-plugin",
				current=self._plugin_version,
				stable_branch=dict(
				    name="Stable", branch="master", comittish=["master"]
				),
				prerelease_branches=[
				    dict(
					name="Release Candidate",
					branch="rc",
					comittish=["rc", "master"],
				    )
				],
				# update method: pip
				pip="https://github.com/Zinc-OS/octoprint-robot-plugin/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "robot control"
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = RobotControlPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.recieved": __plugin_implementation__.gcode_set_angle
	}
