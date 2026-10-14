.class public Lat/stempeluhr/app/Bridge;
.super Ljava/lang/Object;

.field private final a:Lat/stempeluhr/app/MainActivity;

.method public constructor <init>(Lat/stempeluhr/app/MainActivity;)V
    .registers 2
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, Lat/stempeluhr/app/Bridge;->a:Lat/stempeluhr/app/MainActivity;
    return-void
.end method

.method public saveFile(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .registers 8
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-object v0, p0, Lat/stempeluhr/app/Bridge;->a:Lat/stempeluhr/app/MainActivity;
    iput-object p3, v0, Lat/stempeluhr/app/MainActivity;->pending:Ljava/lang/String;
    new-instance v1, Landroid/content/Intent;
    const-string v2, "android.intent.action.CREATE_DOCUMENT"
    invoke-direct {v1, v2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
    const-string v2, "android.intent.category.OPENABLE"
    invoke-virtual {v1, v2}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;
    invoke-virtual {v1, p2}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;
    const-string v2, "android.intent.extra.TITLE"
    invoke-virtual {v1, v2, p1}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;
    new-instance v2, Lat/stempeluhr/app/Starter;
    const/4 v3, 0x1
    invoke-direct {v2, v0, v1, v3}, Lat/stempeluhr/app/Starter;-><init>(Lat/stempeluhr/app/MainActivity;Landroid/content/Intent;I)V
    invoke-virtual {v0, v2}, Lat/stempeluhr/app/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V
    return-void
.end method

.method public openFile()V
    .registers 5
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-object v0, p0, Lat/stempeluhr/app/Bridge;->a:Lat/stempeluhr/app/MainActivity;
    new-instance v1, Landroid/content/Intent;
    const-string v2, "android.intent.action.OPEN_DOCUMENT"
    invoke-direct {v1, v2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
    const-string v2, "android.intent.category.OPENABLE"
    invoke-virtual {v1, v2}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;
    const-string v2, "*/*"
    invoke-virtual {v1, v2}, Landroid/content/Intent;->setType(Ljava/lang/String;)Landroid/content/Intent;
    new-instance v2, Lat/stempeluhr/app/Starter;
    const/4 v3, 0x2
    invoke-direct {v2, v0, v1, v3}, Lat/stempeluhr/app/Starter;-><init>(Lat/stempeluhr/app/MainActivity;Landroid/content/Intent;I)V
    invoke-virtual {v0, v2}, Lat/stempeluhr/app/MainActivity;->runOnUiThread(Ljava/lang/Runnable;)V
    return-void
.end method

.method public getImported()Ljava/lang/String;
    .registers 4
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-object v0, p0, Lat/stempeluhr/app/Bridge;->a:Lat/stempeluhr/app/MainActivity;
    iget-object v1, v0, Lat/stempeluhr/app/MainActivity;->imported:Ljava/lang/String;
    const/4 v2, 0x0
    iput-object v2, v0, Lat/stempeluhr/app/MainActivity;->imported:Ljava/lang/String;
    return-object v1
.end method

.method public copy(Ljava/lang/String;)V
    .registers 5
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-object v0, p0, Lat/stempeluhr/app/Bridge;->a:Lat/stempeluhr/app/MainActivity;
    iget-object v0, v0, Lat/stempeluhr/app/MainActivity;->clip:Landroid/content/ClipboardManager;
    if-eqz v0, :end
    const-string v1, "Stempeluhr"
    invoke-static {v1, p1}, Landroid/content/ClipData;->newPlainText(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Landroid/content/ClipData;
    move-result-object v1
    invoke-virtual {v0, v1}, Landroid/content/ClipboardManager;->setPrimaryClip(Landroid/content/ClipData;)V
    :end
    return-void
.end method

.method public exit()V
    .registers 3
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-object v0, p0, Lat/stempeluhr/app/Bridge;->a:Lat/stempeluhr/app/MainActivity;
    const/4 v1, 0x1
    invoke-virtual {v0, v1}, Lat/stempeluhr/app/MainActivity;->moveTaskToBack(Z)Z
    return-void
.end method
