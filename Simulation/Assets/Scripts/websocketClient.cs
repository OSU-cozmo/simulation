using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Net.Sockets;

public class websocketClient : MonoBehaviour {

	public WebSocket w;
	public int port = 8765;
	int deltaT = 0;
	IEnumerator Start() {
		w = new WebSocket(new Uri(String.Format("ws://localhost:{0}", port)));
		yield return StartCoroutine(w.Connect());
		Debug.Log("sending str");
		w.SendString("handshake successful");
		int i = 0;
		while (true) {
			string reply = w.RecvString();
			if (reply != null) {
				Debug.Log(reply);
				w.SendString("Recieved message");
			}

			yield return i;

		}
		w.Close();

	}

	public void Update() {
		deltaT++;
		//Send stop command after update happened 300 times
		if (deltaT > 300) {
			w.SendString("stop");
		}
	}
}
