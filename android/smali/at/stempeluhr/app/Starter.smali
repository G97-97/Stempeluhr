.class public Lat/stempeluhr/app/Starter;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;

.field private final a:Lat/stempeluhr/app/MainActivity;
.field private final i:Landroid/content/Intent;
.field private final c:I

.method public constructor <init>(Lat/stempeluhr/app/MainActivity;Landroid/content/Intent;I)V
    .registers 4
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, Lat/stempeluhr/app/Starter;->a:Lat/stempeluhr/app/MainActivity;
    iput-object p2, p0, Lat/stempeluhr/app/Starter;->i:Landroid/content/Intent;
    iput p3, p0, Lat/stempeluhr/app/Starter;->c:I
    return-void
.end method

.method public run()V
    .registers 4
    :try_start
    iget-object v0, p0, Lat/stempeluhr/app/Starter;->a:Lat/stempeluhr/app/MainActivity;
    iget-object v1, p0, Lat/stempeluhr/app/Starter;->i:Landroid/content/Intent;
    iget v2, p0, Lat/stempeluhr/app/Starter;->c:I
    invoke-virtual {v0, v1, v2}, Lat/stempeluhr/app/MainActivity;->startActivityForResult(Landroid/content/Intent;I)V
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch
    return-void
    :catch
    move-exception v0
    return-void
.end method
