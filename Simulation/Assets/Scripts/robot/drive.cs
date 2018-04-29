using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class drive : MonoBehaviour {
	public int direction = 0;
	public float distance = 0;
	public Vector3 startPos;
	public Rigidbody rb;
	// Use this for initialization
	void Start () {
		startPos = this.transform.position;
		
	}
	
	// Update is called once per frame
	void Update () {
		if(distance <= 0 || direction == 0) {
			rb.velocity = Vector3.zero;
		} else {
			this.distance -= Vector3.Distance(this.transform.position, this.startPos);
		}
	}

	public void driveForward(float dist, float speed) {
		this.startPos = this.transform.position;
		this.direction = 1;
		this.distance = dist;
		this.rb.AddRelativeForce(Vector3.forward * speed);
	}
}
