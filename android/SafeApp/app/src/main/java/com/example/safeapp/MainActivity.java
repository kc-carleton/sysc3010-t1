package com.example.safeapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    private EditText username;
    private EditText password;
    private TextView info;
    private Button login;

    private final String ADMIN_USERNAME = "a";
    private String ADMIN_PASSWORD = "p";
    private int login_fail_counter;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        username = (EditText)findViewById(R.id.editUsername);
        password = (EditText)findViewById(R.id.editPassword);
        info = (TextView) findViewById(R.id.txtLogin);
        login = (Button) findViewById(R.id.btnLogin);

        info.setText("Please login!");
        login_fail_counter = 0;

        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                username.onEditorAction(EditorInfo.IME_ACTION_DONE);
                password.onEditorAction(EditorInfo.IME_ACTION_DONE);
                validateLogin(username.getText().toString(), password.getText().toString());
            }
        });

    }

    private void validateLogin(String un, String pw) {
        if(un.equals(ADMIN_USERNAME) && pw.equals(ADMIN_PASSWORD)) {
            Intent intent = new Intent(MainActivity.this, adminControls.class);
            startActivity(intent);
        } else {
            login_fail_counter += 1;
            info.setText(String.format("Failed to login %s times, please try again", login_fail_counter));
        }
    }
}
