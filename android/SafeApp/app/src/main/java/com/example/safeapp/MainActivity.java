package com.example.safeapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

/**
 * MainActivity is the starting class for application
 * This class validates the login and proceeds to the admin controls
 */
public class MainActivity extends AppCompatActivity {

    private EditText username;
    private EditText password;
    private Button login;

    private final String ADMIN_USERNAME = "admin";
    private String ADMIN_PASSWORD = "pw";

    /**
     * Loads the screen
     * @param savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        username = (EditText)findViewById(R.id.editUsername);
        password = (EditText)findViewById(R.id.editPassword);
        login = (Button) findViewById(R.id.btnLogin);

        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                username.onEditorAction(EditorInfo.IME_ACTION_DONE);
                password.onEditorAction(EditorInfo.IME_ACTION_DONE);
                validateLogin(username.getText().toString(), password.getText().toString());
            }
        });

    }

    /**
     * Validates the username and password combo
     * @param un username to validate
     * @param pw password to validate
     */
    private void validateLogin(String un, String pw) {
        if(un.equals(ADMIN_USERNAME) && pw.equals(ADMIN_PASSWORD)) {
            Intent intent = new Intent(MainActivity.this, AdminControls.class);
            startActivity(intent);
        } else {
            Toast.makeText(this, String.format("Failed to login, please try again"), Toast.LENGTH_LONG).show();
        }
    }
}
