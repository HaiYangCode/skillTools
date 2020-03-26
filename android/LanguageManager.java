package ex.com.bksbex.common.utils;

import android.annotation.TargetApi;
import android.content.Context;
import android.content.res.Configuration;
import android.content.res.Resources;
import android.os.Build;
import android.util.DisplayMetrics;

import com.tencent.mmkv.MMKV;

import java.util.Locale;


public class LanguageManager {

    private static final String SELECTED_LANGUAGE = "selected_language";

    private static LanguageManager instance;

    private Context mContext;

    public static void init(Context mContext) {
        if (instance == null) {
            synchronized (LanguageManager.class) {
                if (instance == null) {
                    instance = new LanguageManager(mContext);
                    instance.updateLocale(Locale.SIMPLIFIED_CHINESE);
                }
            }
        }
    }

    public static LanguageManager getInstance() {
        if (instance == null) {
            throw new IllegalStateException("You must be init LanguageManager first");
        }
        return instance;
    }

    private LanguageManager(Context context) {
        this.mContext = context;
    }

    public void setConfiguration() {
        Locale targetLocale = getLocale();
        Configuration configuration = mContext.getResources().getConfiguration();

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            configuration.setLocale(targetLocale);
        } else {
            configuration.locale = targetLocale;
        }

        Resources resources = mContext.getResources();
        DisplayMetrics dm = resources.getDisplayMetrics();
        resources.updateConfiguration(configuration, dm);
    }

    public Locale getLocale() {
        MMKV mmkv = MMKV.defaultMMKV();
        String language = mmkv.getString("SELECTED_LANGUAGE", SELECTED_LANGUAGE);
        if (language == null || language.trim().equals("")) {
            language = Locale.getDefault().getLanguage();//没有设置过语言，就获取系统语言；
        }
        return new Locale(language);
    }

    public void updateLocale(Locale locale) {
        MMKV mmkv = MMKV.defaultMMKV();
        mmkv.putString("SELECTED_LANGUAGE", locale.getLanguage());
        this.setConfiguration();
    }

    public static Context attachBaseContext(Context context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            return createConfigurationResources(context);
        } else {
            LanguageManager.getInstance().setConfiguration();
            return context;
        }
    }

    @TargetApi(Build.VERSION_CODES.N)
    private static Context createConfigurationResources(Context context) {
        Resources resources = context.getResources();
        Configuration configuration = resources.getConfiguration();
        Locale locale = getInstance().getLocale();
        configuration.setLocale(locale);
        return context.createConfigurationContext(configuration);
    }

}
