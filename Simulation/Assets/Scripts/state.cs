using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class state : MonoBehaviour {
	public class stateInfo {
		public Vector3 position, rotation;
		public stateInfo(Vector3 pos, Vector3 rot) {
			this.position = pos;
			this.rotation = rot;
		}
	}


	public string getJSON() {
		stateInfo temp = new stateInfo(this.transform.position, this.transform.rotation.eulerAngles);

		return JsonUtility.ToJson(temp);
	}
}
