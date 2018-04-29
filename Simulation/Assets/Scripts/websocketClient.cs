using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Net.Sockets;

public class websocketClient : MonoBehaviour {

	public WebSocket w;
	public int port = 8765;
	public List<GameObject> Recievers;
	int sent = 0;
	int deltaT = 0;
	int waiting = 0;
	bool done = false;
	bool init = false;
	bool ready = false;
	IEnumerator Start() {
		w = new WebSocket(new Uri(String.Format("ws://localhost:{0}", port)));
		yield return StartCoroutine(w.Connect());
		string msg = buildInitMessage();
		//Debug.Log(msg);
		w.SendString(msg);
		int i = 0;
		while (true) {
			string reply = w.RecvString();
			sent++;
			if (reply != null) {
				this.route(reply);
			}

			yield return i;
		}
	}

	public void Update() {
		deltaT++;

		//Send stop command after update happened 300 times
		if (deltaT > 400 && !done) {
			stop();
		}
	}

	private void route(string msg) {
		Debug.Log("routing " + msg);
		Response res = JsonUtility.FromJson<Response>(msg);
		if (res != null) {
			Debug.Log(res.ready);
			if ((res.ready && waiting != 0) || res.type == "INIT_S") {
				getNext();
			}
		}
	}

	private void stop() {
		header stopper = new header();
		stopper.build("STOP", "Stopping the server", sent);
		string msg = "JSON{\"header\":" + JsonUtility.ToJson(stopper) + ",\"body\":{}}";
		//Debug.Log(msg);
		w.SendString(msg);
		done = true;
	}
	private void getNext() {
		//Debug.Log("getting next");
		header next = new header();
		next.build("NEXT", "Getting the next command", sent);
		string msg = "JSON{\"header\":" + JsonUtility.ToJson(next) + ",\"body\":{}}";
		w.SendString(msg);
		waiting = 0;
		
	}
	private string buildInitMessage() {
		initMsg msg = new initMsg(this.Recievers);
		return msg.getJson();
	}
}

public class initMsg {
	public header header;
	public List<obj> objects;
	public class obj {
		public int index;
		public string name;
		public Vector3 position, rotation;

		public obj(GameObject obj, int index) {
			this.name = obj.name;
			this.index = index;
			this.position = obj.transform.position;
			this.rotation = obj.transform.rotation.eulerAngles;
		}

		public string getJSON() {

			return JsonUtility.ToJson(this);
		}
	}
	public initMsg(List<GameObject> obs) {
		header = new header();
		header.build("INIT", "initializing world", 0);
		objects = new List<obj>();
		for (int i = 0; i < obs.Count; i++) {
			objects.Add(new obj(obs[i], i));
		}
	}

	public string getJson() {
		string msg = "JSON{\"header\":";
		msg += JsonUtility.ToJson(this.header);
		msg += ",\"body\":{\"objects\":[";
		for(int i = 0; i < objects.Count; i++) {
			msg += objects[i].getJSON();
			if (i != objects.Count - 1)
				msg += ',';
		}
		msg += "]}}";
		return msg;
	}

}

public class header {
	public string type, msg;
	public int seq;
	public header() { 
	}

	public void build(string type, string msg, int seq) {
		this.type = type;
		this.msg = msg;
		this.seq = seq;
	}
}

[Serializable]
public class Response {

	public string type, msg;
	public int seq;

	public bool ready;
	public string command;


}
