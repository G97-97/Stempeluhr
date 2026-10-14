.class public Lat/stempeluhr/app/MainActivity;
.super Landroid/app/Activity;

.field public wv:Landroid/webkit/WebView;
.field public pending:Ljava/lang/String;
.field public imported:Ljava/lang/String;
.field public clip:Landroid/content/ClipboardManager;

.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .registers 6
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    invoke-virtual {p0}, Lat/stempeluhr/app/MainActivity;->getWindow()Landroid/view/Window;
    move-result-object v0
    const v1, -0xf194a9
    invoke-virtual {v0, v1}, Landroid/view/Window;->setStatusBarColor(I)V

    const-string v0, "clipboard"
    invoke-virtual {p0, v0}, Lat/stempeluhr/app/MainActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Landroid/content/ClipboardManager;
    iput-object v0, p0, Lat/stempeluhr/app/MainActivity;->clip:Landroid/content/ClipboardManager;

    new-instance v0, Landroid/webkit/WebView;
    invoke-direct {v0, p0}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V
    iput-object v0, p0, Lat/stempeluhr/app/MainActivity;->wv:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;
    move-result-object v1
    const/4 v2, 0x1
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setAllowFileAccess(Z)V

    new-instance v1, Landroid/webkit/WebViewClient;
    invoke-direct {v1}, Landroid/webkit/WebViewClient;-><init>()V
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    new-instance v1, Lat/stempeluhr/app/Bridge;
    invoke-direct {v1, p0}, Lat/stempeluhr/app/Bridge;-><init>(Lat/stempeluhr/app/MainActivity;)V
    const-string v2, "AndroidBridge"
    invoke-virtual {v0, v1, v2}, Landroid/webkit/WebView;->addJavascriptInterface(Ljava/lang/Object;Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lat/stempeluhr/app/MainActivity;->setContentView(Landroid/view/View;)V

    const-string v1, "file:///android_asset/index.html"
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V
    return-void
.end method

.method public onBackPressed()V
    .registers 4
    iget-object v0, p0, Lat/stempeluhr/app/MainActivity;->wv:Landroid/webkit/WebView;
    const-string v1, "window.__onBack ? window.__onBack() : AndroidBridge.exit()"
    const/4 v2, 0x0
    invoke-virtual {v0, v1, v2}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V
    return-void
.end method

.method private toast(Ljava/lang/String;)V
    .registers 4
    const/4 v0, 0x0
    invoke-static {p0, p1, v0}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;
    move-result-object v1
    invoke-virtual {v1}, Landroid/widget/Toast;->show()V
    return-void
.end method

.method protected onActivityResult(IILandroid/content/Intent;)V
    .registers 10
    invoke-super {p0, p1, p2, p3}, Landroid/app/Activity;->onActivityResult(IILandroid/content/Intent;)V
    const/4 v0, -0x1
    if-ne p2, v0, :end
    if-eqz p3, :end
    invoke-virtual {p3}, Landroid/content/Intent;->getData()Landroid/net/Uri;
    move-result-object v0
    if-eqz v0, :end

    :try_start
    invoke-virtual {p0}, Lat/stempeluhr/app/MainActivity;->getContentResolver()Landroid/content/ContentResolver;
    move-result-object v1
    const/4 v2, 0x1
    if-ne p1, v2, :read

    invoke-virtual {v1, v0}, Landroid/content/ContentResolver;->openOutputStream(Landroid/net/Uri;)Ljava/io/OutputStream;
    move-result-object v1
    iget-object v2, p0, Lat/stempeluhr/app/MainActivity;->pending:Ljava/lang/String;
    const-string v3, "UTF-8"
    invoke-virtual {v2, v3}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B
    move-result-object v2
    invoke-virtual {v1, v2}, Ljava/io/OutputStream;->write([B)V
    invoke-virtual {v1}, Ljava/io/OutputStream;->close()V
    const-string v1, "Datei gespeichert"
    invoke-direct {p0, v1}, Lat/stempeluhr/app/MainActivity;->toast(Ljava/lang/String;)V
    goto :ok

    :read
    invoke-virtual {v1, v0}, Landroid/content/ContentResolver;->openInputStream(Landroid/net/Uri;)Ljava/io/InputStream;
    move-result-object v1
    new-instance v2, Ljava/io/ByteArrayOutputStream;
    invoke-direct {v2}, Ljava/io/ByteArrayOutputStream;-><init>()V
    const/16 v3, 0x2000
    new-array v3, v3, [B
    :loop
    invoke-virtual {v1, v3}, Ljava/io/InputStream;->read([B)I
    move-result v4
    if-lez v4, :done
    const/4 v5, 0x0
    invoke-virtual {v2, v3, v5, v4}, Ljava/io/ByteArrayOutputStream;->write([BII)V
    goto :loop
    :done
    invoke-virtual {v1}, Ljava/io/InputStream;->close()V
    const-string v3, "UTF-8"
    invoke-virtual {v2, v3}, Ljava/io/ByteArrayOutputStream;->toString(Ljava/lang/String;)Ljava/lang/String;
    move-result-object v2
    iput-object v2, p0, Lat/stempeluhr/app/MainActivity;->imported:Ljava/lang/String;
    iget-object v2, p0, Lat/stempeluhr/app/MainActivity;->wv:Landroid/webkit/WebView;
    const-string v3, "window.__onImport && window.__onImport()"
    const/4 v4, 0x0
    invoke-virtual {v2, v3, v4}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch

    :ok
    :end
    return-void

    :catch
    move-exception v1
    const-string v1, "Datei konnte nicht verarbeitet werden"
    invoke-direct {p0, v1}, Lat/stempeluhr/app/MainActivity;->toast(Ljava/lang/String;)V
    return-void
.end method
