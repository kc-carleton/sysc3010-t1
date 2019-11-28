package com.example.safeapp;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;

import java.util.ArrayList;

public class UserList extends ArrayAdapter<User> {

    private Activity context;
    private ArrayList<User> users;

    public UserList(Activity context, ArrayList<User> users) {
        super(context, R.layout.layout_user_list, users);
        this.context = context;
        this.users = users;
    }

    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = context.getLayoutInflater();
        View listViewItem = inflater.inflate(R.layout.layout_user_list, null, true);

        TextView textUsername = (TextView) listViewItem.findViewById(R.id.textUsername);
        TextView textUsercode = (TextView) listViewItem.findViewById(R.id.textUsercode);

        User user = users.get(position);
        textUsername.setText(user.getUser_name());
        textUsercode.setText(Integer.toString(user.getUser_code()));

        return listViewItem;
    }
}
