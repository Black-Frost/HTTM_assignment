package com.lampa.emotionrecognition;

import com.lampa.emotionrecognition.utils.*;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.Rect;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Base64;
import java.util.Map;
import java.util.Objects;

import okhttp3.*;

public class Classifier {
    public String host;
    private Handler mHandler;
    public OkHttpClient client;
    public static final MediaType JSON
            = MediaType.get("application/json; charset=utf-8");

    Classifier(String url) {
        host = url;
        mHandler = new Handler(Looper.getMainLooper());
        client = new OkHttpClient();
    }

    void detectFaces(Bitmap imageBitmap, DrawBorderCallback callback) {
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        imageBitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);
        byte[] byteArray = stream.toByteArray();

        String b64Image = new String(Base64.getEncoder().encode(byteArray));

        JSONObject imageJson = new JSONObject();
        try {
            imageJson.put("image", b64Image);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        RequestBody body = RequestBody.create(imageJson.toString(), JSON);
        Request request = new Request.Builder()
                .url(host + "/api/v1/face-detect/")
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
                //Log.d("Response-frost", response.body().string());
                try {
                    JSONObject Jobject = new JSONObject(response.body().string());
                    JSONArray faceList = Jobject.getJSONArray("faces");
                    List<Rect> faceRectList = new ArrayList<Rect>();

                    for (int i = 0; i < faceList.length(); i++) {
                        JSONObject obj = faceList.getJSONObject(i);
                        int bottom = obj.getInt("bottom");
                        int top = obj.getInt("top");
                        int left = obj.getInt("left");
                        int right = obj.getInt("right");

                        faceRectList.add(new Rect(left, top, right, bottom));
                    }
                    mHandler.post(() -> callback.exec(imageBitmap, faceRectList));

                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        });
    }

    void classifyEmotions(List<Bitmap> faceBitmapList, UpdateEmotionListCallback callback) {

        JSONArray imgArray = new JSONArray();
        for (Bitmap faceBitmap : faceBitmapList) {
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            faceBitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);
            byte[] byteArray = stream.toByteArray();

            String b64Image = new String(Base64.getEncoder().encode(byteArray));
            imgArray.put(b64Image);
        }
        JSONObject imageJson = new JSONObject();
        try {
            imageJson.put("images", imgArray);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        RequestBody body = RequestBody.create(imageJson.toString(), JSON);
        Request request = new Request.Builder()
                .url(host + "/api/v1/emotion/")
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
                //Log.d("Response-frost", response.body().string());
                try {
                    List<Map<String, Float>> guiEmotionData = new ArrayList<>();
                    JSONArray emotionJson = new JSONArray(response.body().string());
                    for (int i = 0; i < emotionJson.length(); i++) {
                        JSONObject faceJson = emotionJson.getJSONObject(i);
                        Map<String, Float> faceEmotionMap = new HashMap<>();
                        Iterator<?> keys = faceJson.keys();
                        while (keys.hasNext()) {
                            String key = (String) keys.next();
                            Float value = (float)faceJson.getDouble(key);
                            faceEmotionMap.put(key,value);
                        }
                        guiEmotionData.add(faceEmotionMap);
                    }
                    mHandler.post(() -> callback.exec(guiEmotionData));

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }
}

