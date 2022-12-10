package com.lampa.emotionrecognition;

import com.lampa.emotionrecognition.utils.*;
import android.graphics.Bitmap;
import android.graphics.Rect;
import android.os.Build;
import android.util.Log;

import androidx.annotation.NonNull;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Base64;
import java.util.Objects;

import okhttp3.*;

public class Classifier {
    public String host;
    public OkHttpClient client;
    public static final MediaType JSON
            = MediaType.get("application/json; charset=utf-8");

    Classifier(String url) {
        this.host = url;
        client = new OkHttpClient();
    }

    public List<Rect> getFaces(Bitmap imageBitmap, DrawBorderCallback callback) {
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        imageBitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);
        byte[] byteArray = stream.toByteArray();

        String b64Image = new String(Base64.getEncoder().encode(byteArray));
        Log.d("Frost-Resquest", b64Image);

        JSONObject imageJson = new JSONObject();
        try {
            imageJson.put("image", b64Image);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        Log.d("Frost", "HERE");
        RequestBody body = RequestBody.create(imageJson.toString(), JSON);
        Request request = new Request.Builder()
                .url(host + "/api/v1/predict/")
                .post(body)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(@NonNull Call call, @NonNull Response response) throws IOException {
                if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);
                Log.d("Response-frost", response.body().toString());
            }
        });

        return new ArrayList<>();
    }
}

